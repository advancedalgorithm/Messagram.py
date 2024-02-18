import enum

"""
	enum Settings_T{}

	Used for readability and bug tracking
"""
class Settings_T(enum.Enum):
	null 			= 0x0000000
	username		= 0x0000001
	email			= 0x0000002
	password		= 0x0000003

	add_trust_sys	= 0x0000007
	rm_trust_sys	= 0x0000008

class TrustSystems_T(enum.Enum):
	null 		  	= 0x0000010
	pin_code		= 0x0000011
	email 		  	= 0x0000012
	phone 		  	= 0x0000013
	authenticator 	= 0x0000014

class Message_T(enum.Enum):
    NULL            = 0x30001
    DM              = 0x30002
    COMMUNITY       = 0x30003

class Message():
    from_username   : str;
    to_username     : str;
    data            : str;
    timestamp       : str;

class Community():
    name            : str;
    roles           : str;
    users           : list;
    messages        : list[Message]

class DM():
    to_username     : str; # If chat_type is Message_T.DM
    messages        : list[Message]

    # MESSAGE_ID,MESSAGE_FROM,MESSAGE_TO,MESSAGE_DATA,MESSAGE_TIMESTAMP,MESSAGE_SENT/SEEN
    def __init__(self, chat_t: Message_T, from_user: str, to: str, d: str):
        self.chat_type = chat_t
        self.from_username = from_user
        self.data = d

        if chat_t == Message_T.DM:
            self.to_username = to
            return

        self.to_chat_id = to

    def get_chat_data(self) -> str:
        return self.data
    
class User():
    user_idx			: int;
    user_id				: str;
    username			: str;
    email				: str;
    password			: str;
    ip_addr				: str;
    sms_number			: str;
    pin_code			: str;
    messa_rank			: int;

    hash                : str;

    """
    	2FA Using Email and//or Phone Number
    """

    twofa_toggle		: bool;
    twofa 				: TrustSystems_T;

    """ 2D Array [ PC_NAME: [] ] """
    trusted_systems		: dict[str, str];
    communities			: list[Community];
    dms 				: list[DM];

    def __init__(self, content: str):
        pass

    def __repr__(self):
        return ""
    
    def __str__(self) -> str:
        return ""