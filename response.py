import json, enum

class Resp_T:
    NULL                            = 0x00000
    
    """ CONNECTION SUCCESS """
    socket_connected                = 0x00001
    
    """ CONNECTION FAILURE """
    invalid_connection              = 0x00002
    socket_rejected                 = 0x00003
    device_banned                   = 0x00004
    
    """ ACTION EVENTS """
    user_resp                       = 0x00005
    push_event                      = 0x00006
    mass_event                      = 0x00007

class Cmd_T(enum.Enum):
    NULL                            = 0x10000
    """
     *                  SERVER COMMANDS & SERVER COMMAND RESPONSES
     * 
     * The developer using this client library only needs to know what these objects
     * are used for in-order to build a better response message for the user on client
     * 
     * !!! The Server will not respond with a neat message to output for users !!!
    """

    """ REQUEST ERRORS """
    invalid_cmd                     = 0x10001
    invalid_parameters              = 0x10002 # INVALID PARAMETERS SENT TO SERVER
    invalid_perm                    = 0x10003 # INVALID PERMS (USED FOR COMMUNITY ROLES ETCS)
    invalid_operation               = 0x10004 # A reason will be sent why. This is more for the developer using the API

    """ 
     * LOGIN CMDS FOR SERVER 
    """
    client_authentication           = 0x10005 # Sending login information

    """ 
     * LOGIN CMD RESPONSES FROM SERVER 
    """
    add_sms_auth                    = 0x10006 # SEND NEW PHONE NUMBER FOR VERIFICATION
    add_new_email                   = 0x10007 # CHANGE CURRENT EMAIL FOR VERIFICATION
    send_pin_verification_code      = 0x10008 # SEND PIN VERIFICATION CODE
    send_sms_verification_code      = 0x10009 # SEND SMS VERIFICATION CODE
    send_email_verification_code    = 0x10010 # SEND EMAIL VERIFICATION CODE

    """ SUCCESS OPERATIONS """
    successful_login                = 0x10011 # LOGIN SUCCESSFUL
    new_email_added                 = 0x10012 # NEW EMAIL HAS BEEN ADDED
    trust_confirm                   = 0x10013 # EMAIL HAS BEEN VERIFIED
    sms_verified                    = 0x10014 # SMS CODE HAS BEEN VERIFIED
    pin_verified                    = 0x10015 # PIN CODE HAS BEEN VERIFIED
    number_added                    = 0x10016 # PHONE NUMBER HAS BEEN ADDED & SMS SENT

    """ FAIL OPERATIONS """
    invalid_login_info              = 0x10017 # INVALID USERNAME OR PASSWORD
    account_perm_ban                = 0x10018 # ACCOUNT PERM BANNED
    account_temp_ban                = 0x10019 # ACCOUNT TEMP BANNED
    force_confirm_email             = 0x10020 # FORCE USER TO VERIFY EMAIL TO USE THE ACCOUNT
    force_device_trust              = 0x10021 # UNKNOWN DEVICE, TRUST CONFIRMATION EMAIL SENT
    force_add_phone_number_request  = 0x10022 # FORCE USER TO ADD A PHONE NUMBER
    verify_pin_code                 = 0x10023 # REQUEST USER FOR PIN CODE
    verify_sms_code                 = 0x10024 # REQUEST USER FOR SMS CODE
    """
     * FRIEND REQUEST CMD FOR SERVER
     * 
     * Due to signals in the response type with a small message
     * objects is not needed for server response. 
     * 
     * The client will only be receiving the following CMD Types on failure:
     *      - INVALID_CMD
     *      - INVALID_PARAMETERS
     *      - INVALID_OPERATION
     *      
     * A better message can be built for response on failure
    """
    send_friend_req                 = 0x10025 # SEND A FRIEND REQUEST
    cancel_friend_req               = 0x10026 # CANCEL A FRIEND REQUEST

    """ SUCCESS OPERATIONS """
    friend_request_sent             = 0x10027 # FRIEND REQUEST SENT
    
    """ FAILED OPERATIONS """
    failed_to_send_friend_request   = 0x10028 # FAILED TO SEND FRIEND REQUEST
    blocked_by_user                 = 0x10029 # FRIEND REQUESTED USER HAS THE CURRENT CLIENT USER BLOCKED

    """ 
     * DM CMD FOR SERVER 
     * 
     * Due to signals in the response type with a small message
     * objects is not needed for server response. 
     * 
     * The client will only be receiving the following CMD Types on failure:
     *      - INVALID_CMD
     *      - INVALID_PARAMETERS
     *      - INVALID_OPERATION
     *      
     * A better message can be built for response on failure
    """
    send_dm_msg                     = 0x10030 # SEND DM MESSAGE
    send_dm_msg_rm                  = 0x10031 # SEND DM MESSAGE REMOVAL
    send_dm_reaction                = 0x10032 # SEND DM REACTION
    send_dm_reaction_rm             = 0x10033 # SEND DM REACTION REMOVAL

    """ OPERATION RESPONSES """
    dm_sent                         = 0x10034 # DM SUCCESSFULLY SENT
    dm_failed                       = 0x10035 # DM FAILED
    """
     * COMMUNITY CMD FOR SERVER
    """

    """ FAILED OPERATIONS """
    invalid_role_perm               = 0x10036 # ROLE DOES NOT CONTAIN PERMISSION FOR OPERATION REQUESTED
    
    """ COMMUNITY CREATION & SETTING EDITING """
    create_community                = 0x10037 # CREATE A COMMUNITY (LIKE A DISCORD SERVER)
    edit_community                  = 0x10038 # Edit Community Info/Settings (EDIT A COMMUNITY SETTINGS OR INFO)
    invo_toggle                     = 0x10039 # Enable/Disable Community Invites (EDIT THE INVITE TOGGLE)
    kick_user                       = 0x10040 # Kick a user from the community
    ban_user                        = 0x10041 # Ban a user from the community
    del_msg                         = 0x10042 # Delete a message from the community chat

    """ Roles """
    create_community_role           = 0x10043 # CREATE A ROLE
    edit_community_role             = 0x10044 # EDIT A ROLE (Perms, Color, Rank Level)
    del_community_role              = 0x10045 # DELETE A ROLE
    
    """ Chats """
    create_community_chat           = 0x10046 # CREATE A NEW CHAT
    edit_community_chat             = 0x10047 # EDIT THE CHAT SETTINGS (Perms, Name, Desc)
    del_community_chat              = 0x10048 # DELETE THE CHAT

    """
     * 
     *          EVENT NOTIFICATIONS
     * 
     * Commands from server, Actions from/by other users
     * 
     * Mainly used for receiving commands from server which is
     * usually when a user requests or msg another user
    """
    account_banned                  = 0x10049 # ACCOUNT BANNED
    friend_req_received             = 0x10050 # USER FRIEND REQUEST HAS BEEN RECEIVED
    dm_msg_received                 = 0x10051 # USER DM MESSAGE HAS BEEN RECEIVED
    community_msg_received          = 0x10052 # COMMUNITY MESSAGED RECEIVED


class Response:
    status          : bool;
    resp_t          : Resp_T;
    cmd_t           : Cmd_T;

    from_username   : str;
    to_username     : str;
    to_chat_id      : str;
    data            : str;

    acc_info        : dict[str, str];
    server_resp     : dict[str, str];
    parameters      : dict[str, str];
    new_cmd         : dict[str, str];
    """ 
        m = Messagram("official_client", "0.0.1")
        r = m.ConnectnAuthorize("Jeff", "testpw123") ## THIS IS A Response CLASS WITH DATA

        Use Examples:
            Response("Invalid username or password provided!", false) # This is a message for client output! (Response.from_username, Response.data)
            Response(server_response, false) # This will parse server response (USED IN THE LISTENER AND SendCMD() FUNCTION FOR MESSAGRAM ACTIONS)
            Response("", True, Resp_T.NULL, Cmd_T.send_dm_msg, m.acc_info, {"from_username": m.username, "to_username": "vibe", "data": "Yo, Whats up dawg ?"}) # BUILDS A NEW CMD FOR SERVER ( m.SendCMD(THE_CMD) )
    """
    def __init__(self, d: str, build_new: bool, r: Resp_T = Resp_T.NULL, c: Cmd_T = Cmd_T.NULL, acc_info: dict[str, str] = {}, parameters: dict[str, str] = {}):
        self.data = d
        self.resp_t = r 
        self.cmd_t = c
        
        # Building a new command for server
        if build_new:
            """
                Checking for the main JSON fields
                {
                	"cmd_t":"SEND_DM_MSG",
                    "username":"Jeff", 
                    "sid":"64738550305683186153328442058584", 
                    "hwid":"{6d9c0696-ba90-11ee-94f1-874gd2f6e6963}", 
                    "client_name":"official_client", 
                    "client_version":"0.0.1", 
                }
            """
            for key in ['username', 'sid', 'hwid', 'client_name', 'client_version']:
                if key not in acc_info: 
                    self.resp_t = Resp_T.user_resp
                    self.cmd_t = Cmd_T.invalid_paramets
                    return
            
            self.acc_info = acc_info
            self.parameters = parameters
            self.BuildNewCmd()

        # Response from Server || If it aint a server response then this will/can be used for client message output
        if d.startswith("{") and d.endswith("}"):
            self.parse_server_response()


    def parse_server_response(self) -> None:
        """

        """
        print(f"{self.data}")
        self.server_resp = json.loads(self.data)
        if "status" in self.server_resp and "resp_t" in self.server_resp:
            self.status = bool(self.server_resp['status'])
            self.resp_t = Response.resp2type(self.server_resp['resp_t'])
            self.cmd_t = Response.cmd2type(self.server_resp['cmd_t'])

        if "from_username" in self.server_resp: self.from_username = self.server_resp['from_username']
        if "to_username" in self.server_resp: self.to_username = self.server_resp['to_username']
        if "data" in self.server_resp: self.data = self.server_resp['data']



    def BuildNewCmd(self) -> str:
        new_info = {"cmd_t": f"{Cmd_T(self.cmd_t).name}".replace("Cmd_T.", ""), 
                    "username": self.acc_info['username'],
                    "sid": self.acc_info['sid'],
                    "hwid": self.acc_info['hwid'],
                    "client_name": self.acc_info['client_name'],
                    "client_version": self.acc_info['client_version'] }
        
        self.new_cmd = new_info
        if len(self.parameters) < 1: return
        for key in self.parameters:
            val = self.parameters[key]
            new_info[key] = val
        
        self.new_cmd = new_info

    """ This isn't needed because the MessagramServer does auto response generation aswell """
    def check_specific_inputs(self) -> None:
        match self.cmd_t:
            case Cmd_T.send_dm_msg:
                if len(self.parameters) != 3:
                    self.cmd_t = Cmd_T.invalid_parameters
                    return
            ## Add more cases below
                
    def to_str(self) -> str:
        return f"{self.new_cmd}"

    @staticmethod
    def resp2type(data: str) -> Resp_T:
        match data:
            case "socket_connected":                    return Resp_T.socket_connected
            case "invalid_connection":                  return Resp_T.invalid_connection
            case "socket_rejected":                     return Resp_T.socket_rejected
            case "device_banned":                       return Resp_T.device_banned
            case "user_resp":                           return Resp_T.user_resp
            case "push_event":                          return Resp_T.push_event
            case "mass_event":                          return Resp_T.mass_event
            

    @staticmethod
    def cmd2type(data: str) -> Cmd_T:
        match data:
            case "client_authentication":               return Cmd_T.client_authentication
            case "add_sms_auth":                        return Cmd_T.add_sms_auth
            case "add_new_email":                       return Cmd_T.add_new_email
            case "send_pin_verification_code":          return Cmd_T.send_pin_verification_code
            case "send_email_verification_code":        return Cmd_T.send_email_verification_code
            case "send_email_verification_code":        return Cmd_T.send_email_verification_code
            case "successful_login":                    return Cmd_T.successful_login
            case "new_email_added":                     return Cmd_T.new_email_added
            case "new_email_added":                     return Cmd_T.new_email_added
            case "trust_confirm":                       return Cmd_T.trust_confirm
            case "sms_verified":                        return Cmd_T.sms_verified
            case "pin_verified":                        return Cmd_T.pin_verified
            case "number_added":                        return Cmd_T.number_added
            case "invalid_login_info":                  return Cmd_T.invalid_login_info
            case "account_perm_ban":                    return Cmd_T.account_perm_ban
            case "account_temp_ban":                    return Cmd_T.account_temp_ban
            case "force_confirm_email":                 return Cmd_T.force_confirm_email
            case "force_device_trust":                  return Cmd_T.force_device_trust
            case "force_add_phone_number_request":      return Cmd_T.force_add_phone_number_request
            case "verify_pin_code":                     return Cmd_T.verify_pin_code
            case "verify_sms_code":                     return Cmd_T.verify_sms_code
            case "send_friend_req":                     return Cmd_T.send_friend_req
            case "cancel_friend_req":                   return Cmd_T.cancel_friend_req
            case "friend_request_sent":                 return Cmd_T.friend_request_sent
            case "failed_to_send_friend_request":       return Cmd_T.failed_to_send_friend_request
            case "blocked_by_user":                     return Cmd_T.blocked_by_user
            case "send_dm_msg":                         return Cmd_T.send_dm_msg
            case "send_dm_msg_rm":                      return Cmd_T.send_dm_msg_rm
            case "send_dm_reaction":                    return Cmd_T.send_dm_reaction
            case "send_dm_reaction_rm":                 return Cmd_T.send_dm_reaction_rm
            case "dm_sent":                             return Cmd_T.dm_sent
            case "dm_failed":                           return Cmd_T.dm_failed
            case "invalid_role_perm":                   return Cmd_T.invalid_role_perm
            case "create_community":                    return Cmd_T.create_community
            case "edit_community":                      return Cmd_T.edit_community
            case "invo_toggle":                         return Cmd_T.invo_toggle
            case "kick_user":                           return Cmd_T.kick_user
            case "ban_user":                            return Cmd_T.ban_user
            case "del_msg":                             return Cmd_T.del_msg
            case "create_community_role":               return Cmd_T.create_community_role
            case "edit_community_role":                 return Cmd_T.edit_community_role
            case "del_community_role":                  return Cmd_T.del_community_role
            case "create_community_chat":               return Cmd_T.create_community_chat
            case "edit_community_chat":                 return Cmd_T.edit_community_chat
            case "del_community_chat":                  return Cmd_T.del_community_chat
            case "account_banned":                      return Cmd_T.account_banned
            case "friend_req_received":                 return Cmd_T.friend_req_received
            case "dm_msg_received":                     return Cmd_T.dm_msg_received
            case "community_msg_received":              return Cmd_T.community_msg_received
            case _:                                     return Cmd_T.NULL
            
        return Cmd_T.NULL

