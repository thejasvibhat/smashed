<?php

require_once(dirname(dirname(dirname(dirname(__FILE__)))) . "/engine/start.php");

global $CONFIG;

error_log ("Request Variables" . print_r($_REQUEST, 1));
error_log ("Seesion Variables" . print_r($_SESSION, 1));

$access_code = get_input ("access_token", "");

if ($access_code == "") {
  echo prepare_postfb_response (array ("message" => "Access Token Required", "status_code" => "401"));
  exit();
 }

$facebook = new Facebook ( array(
				 'appId'  => getenv ('FACEBOOK_APPID'),
				 'secret' => getenv ('FACEBOOK_SECRET')
				 ));
$facebook->setAccessToken ($access_code);

error_log ("Facebook object" . print_r($facebook, 1));

try {
  $user_profile = $facebook->api('/me');
} catch (FacebookApiException $e) {
  echo prepare_postfb_response (array ("message" => "Login Failed", "status_code" => "401"));
  exit();
  }

$fbuid = $user_profile['id'];

error_log (print_r ($user_profile, 1));

if (!($fbuid)) {
  echo prepare_postfb_response (array ("message" => "Login Failed", "status_code" => "402"));
  exit();
 }

$entities = get_entities_from_metadata ('xauth_facebook_uid', $fbuid, 'user', 'xauth_facebook');

if ($entities && $entities[0]->enabled == 'yes') {
  $user = $entities[0];
  if ( isset ($user->banned) && $user->banned == 'yes') { // this needs to change.
    echo prepare_postfb_response (array ("message" => "User Banned", "status_code" => "400"));
    exit();
  }

  login ($user);
  echo prepare_postfb_response (array ("message" => "Login Success", "status_code" => "200"));
  exit ();
 }

if ($entities && $entities[0]->enabled == 'no') {
  echo prepare_postfb_response (array ("message" => "Inactive User", "status_code" => "400"));
  exit ();
 }

/* New User */

$user_ent = get_user_by_email ($user_profile['email']);
if ($user_ent[0]) {
  $elgg_user = new ElggUser ($user_ent[0]);
  login ($elgg_user);
  echo prepare_postfb_response (array ("message" => "Login Success", "status_code" => "200"));
  exit();
 }

if (is_allowed_location () == FALSE) {
  echo prepare_postfb_response (array ("message" => "Currently not available in your region", "status_code" => "400"));
  exit(0);
 }

$user = new ElggUser ();
$user->name      = $user_profile['name'];
$user->email     = $user_profile['email'];
$user->agegroup  = get_agegroup_from_dob ($user_profile['birthday']);
$user->password  = "null";
$user->salt      = "null";
$user->access_id = ACCESS_PUBLIC;
$user->subtype   = 'xauth_facebook';
if (isset($user_profile['username']))
  $user->username  = $user_profile['username'] . "_fbk";
else
  $user->username = "fbk_" . $user_profile['id'];
$user->xauth_facebook_uid = $fbuid;
$user->facebook_controlled_profile = 'yes';
$user->validated_email = '1';
if ($user->save() == false) {
  echo prepare_postfb_response (array ("message" => "Username not available.",
				       "status_code" => "400"));
  forward ($_SERVER['HTTP_REFERER']);
 }
//TODO: Improvise

//TODO: User image and location.
login ($user);

create_metadata ($user->guid, 'validated_email', true,'', 0, ACCESS_PUBLIC);

$invitecode = get_input  ("invitecode", "");
if ($invitecode == "" || $invitecode == "0-0") {
  $invite_obj = new fc_invite_entity();
  $invite_obj->get_by_invite_code ($invitecode);

  if ($invite_obj->status == "sent") {
    $invite_obj->update_status ("registered", $user->guid);
  }

  if ($invite_obj->status == "sent") {
    if ($invite_obj->sender_guid != "2") { // Don't add as friend if its invited by admin
      user_add_friend ($user->guid, $invite_obj->sender_guid);
      user_add_friend ($invite_obj->sender_guid, $user->guid);
    }
  }
 }

trigger_elgg_event ("validate", "user", $user);
echo prepare_postfb_response (array ("message" => "Login Success", "status_code" => "200"));

exit ();

function prepare_postfb_response ($arr)
{
  header ("Content-type: text/xml");

  $xml_output  = "<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>";
  $xml_output .= "<fonerap>\n";
  $xml_output .= "<qzresponse>";
  $xml_output .= "<requestapi>PostFB</requestapi>\n";
  $xml_output .= array2xml ($arr);
  $xml_output .= "</qzresponse>";
  $xml_output .= "<qzmessage>Success</qzmessage><qzstatus_code>200</qzstatus_code>";
  $xml_output .= "</fonerap>\n";

  error_log (print_r($xml_output, 1));
  return $xml_output;
}

?>