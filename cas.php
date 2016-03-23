<?php

/**
 * CAS Client Light
 * ----------------
 * Designed to be a single lightweight class for easily integrating CAS
 * authentication into PHP projects.
 *
 * Created by Chris Gibbs on 2009.07.16
 * Copyright Abilene Christian University
 */

global $cas_server_config;
$cas_server_config = array(
	'protocol' => 'https',
	'hostname' => 'sso.acu.edu',
	'login_uri' => '/login',
	'validate_uri' => '/serviceValidate',
	'logout_uri' => '/logout',
	'logout_requesters' => array(
		'malta.acu.edu',
		'hebron.acu.edu'
	)
);

class Acu_cas {


	/**
	 * Gets the authenticated user's username from their session. If the user
	 * isn't already authenticated then it needs to be checked.
	 *
	 * @param boolean $require_auth
	 */
	function get_username($require_auth = false) {
		if (!isset($_SESSION)) session_start();
		//error_log("CAS_Client_Light::get_username() - Session ID: ".session_id());
		if (isset($_SESSION['cas_username'])) {
			//error_log("CAS_Client_Light::get_username() - Found username in session: {$_SESSION['cas_username']}");
			return $_SESSION['cas_username'];
		} else if ($require_auth) {
			//error_log("CAS_Client_Light::get_username() - No username found in session");
			return self::require_auth();
		}
	}


	/**
	 * Requires that the user either be authenticated or have a ticket to validate,
	 * otherwise they are sent to CAS to authenticate.
	 *
	 * @return string $username
	 */
	function require_auth() {
		if (!isset($_SESSION)) session_start();
		if (!isset($_SESSION['cas_username'])) {
			if (isset($_GET['ticket'])) {
				// Validate ticket
				$username = self::validate_service_ticket($_GET['ticket']);
				if (empty($username))
					self::send_to_cas_server();
				else {
					$st = preg_replace('/\W/', '', $_GET['ticket']);
					session_destroy();
					session_id($st);
					session_start();
					$_SESSION['cas_username'] = $username;
					return $username;
				}
			} else {
				// Redirect user to CAS server
				//error_log("CAS_Client_Light::get_username() - No CAS ticket found; Redirecting to CAS server");
				self::send_to_cas_server();
			}
		}
	}


	/**
	 * Creates the service URL for CAS to redirect to after authentication
	 *
	 * @return string $url
	 */
	function get_service_url() {

		if ($_SERVER['SERVER_PORT'] == 80) {
			$url = 'http://' . $_SERVER['SERVER_NAME'];
		} else {
			if ($_SERVER['SERVER_PORT'] == 443)
				$url = 'https://';
			else
				$url = 'http://';
			$url .= $_SERVER['SERVER_NAME'] . ':' . $_SERVER['SERVER_PORT'];
		}
		$url .= $_SERVER['REQUEST_URI'];

		return $url;
	}


	/**
	 * Redirects a user to the CAS login URL
	 */
	function send_to_cas_server() {
		global $cas_server_config;

		$service_url = urlencode(self::get_service_url());

		// Store for validating after redirect
		$_SESSION['cas_service_url'] = $service_url;

		// Redirect
		$url = $cas_server_config['protocol'].'://'.$cas_server_config['hostname'].$cas_server_config['login_uri']."?service=$service_url";
		header("Location: $url");
	}


	/**
	 * Takes a user's service ticket and validates it with the configured
	 * CAS server to ensure authenticity. If it's real, the user's username
	 * is returned.
	 *
	 * @param string $st
	 * @return string $username
	 */
	function validate_service_ticket($st) {
		global $cas_server_config;

		// Get response from CAS
		$service_url = $_SESSION['cas_service_url'];
		$validate_url = $cas_server_config['protocol'].'://'.$cas_server_config['hostname'] . $cas_server_config['validate_uri'] . "?ticket=$st&service=$service_url";
		$cas_response = file_get_contents($validate_url);

		// Parse XML response from CAS
		$parser = xml_parser_create();
		xml_parse_into_struct($parser, $cas_response, $values);
		xml_parser_free($parser);
		if ($values[1]['tag'] == 'CAS:AUTHENTICATIONSUCCESS') {
			// Return the username
			return $values[2]['value'];
		} else {
			return null;
		}
	}


	/**
	 * Handler for unauthenticating a user; locally or via remote POST from
	 * the CAS server.
	 */
	function logout() {
		if (self::is_remote_logout())
			self::remote_logout();
		else
			self::local_logout();
	}


	/**
	 * Invalidates the session user name and redirects to CAS logout URL
	 */
	function local_logout() {
		global $cas_server_config;
		// $_SESSION['cas_username'] = null;
		header("Location: " . $cas_server_config['protocol'].'://'.$cas_server_config['hostname'] . $cas_server_config['logout_uri'] . '?service=http://vote.acu.edu/');
		exit;
	}


	/**
	 * Checks if the HTTP request is a logout POST from the CAS server
	 *
	 * @return boolean
	 */
	function is_remote_logout() {
		return !empty($_POST['logoutRequest']);
	}


	/**
	 * Loads a session specified by the POST from the CAS server and
	 * invalidates it.
	 */
	function remote_logout() {
		// Validate request source
		global $cas_server_config;
		$client_host = gethostbyaddr($_SERVER['REMOTE_ADDR']);
		if (!in_array($client_host, $cas_server_config['logout_requesters'])) {
			error_log("Recieved invalid logout request from $client_host ({$_SERVER['REMOTE_ADDR']})");
			return;
		}

		// Get service ticket from SAML POST
		$saml_request = stripslashes($_POST['logoutRequest']);
		$parser = xml_parser_create();
		xml_parse_into_struct($parser, $saml_request, $values);
		xml_parser_free($parser);
		if (empty($values)) {
			error_log("Invalid SAML request:");
			error_log($_POST['logoutRequest']);
			return;
		}
		$st = preg_replace('/\W/', '', $values[2]['value']);

		// Destroy session with an ID of the ST
		session_id($st);
		$_COOKIE[session_name()]=$st;
		$_GET[session_name()]=$st;
		//session_start();
		session_unset();
		session_destroy();
	}
}
$cas = new Acu_cas();
if(!isset($_GET['logout'])){
	$cas->get_username(true);
	if(isset($_SESSION['cas_username'])){
		header('location: gate/voter_login');
	}
}
else{
	session_start();
	unset($_SESSION['cas_username']);
	session_destroy();
	$cas->local_logout();
}
?>