import config
from messages import Message
from users import Admin, User
import db_functions as db

class Action(User):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.action = None


class DBAction(Action):
    def __init__(self, user_id, obj):
        super().__init__(user_id)
        self.obj = obj
        if self.obj == 'user':
            self.table = config.UsersTable()
        elif self.obj == 'admin':
            self.table = config.AdminsTable()
        elif self.obj == 'coupon':
            self.table = config.AdminCouponsTable(user_id)
        elif self.obj == 'points':
            self.table = config.AdminPointsTable
        self.data = None
        self.query = db.Query(self.table)

    def save_value(self, value, id_col, col_to_change, id_col_value):
        db.UpdateValue(self.user_id, value, id_col, col_to_change, id_col_value)
        self.query.execute()


    def insert_raw(self, values):
        db.InsertRaw(values, self.user_id)
        self.query.execute()


class BotAction(Action, Message):
    def sendmessage(self, message, bot):
        bot.send_message(message.chat.id, self.text, reply_markup=self.markup, parse_mode='html')

    def userinput(self, message, next_def, obj, fieldname, bot):
        self.sendmessage(message,bot)
        bot.register_next_step_handler(message, next_def, obj, fieldname)

    def next_def(self, message, obj, fieldname):
        self.action = DBAction(message.chat.id, obj)
        self.action.save_value(message.text, 'id', fieldname, self.user_id)


class UserInput(BotAction, Message):
    def __init__(self, user_id):
        super().__init__(user_id)

    def send_question(self, message, bot):
        self.sendmessage(message, bot)
        bot.register_next_step_handler(message, self.nextdef)

    def next_def(self):
        pass




# User(id)- UserCategories
# UserUser(user)
# UserAdmin(user)
# UserClient(user)
# UserSuperAdmin(user)

# user = User(user_id)
# action = Action(user_id)
# object = Object(user_id)

# db_admins = DataBase(user_id, 'our clients')
# db = Database(user_id)
# action = db.action
# dbaction.GetRaw(user_id,

# db_admins.action
# action.SendMessage(user_id, object)

# class Action():

# GetAdminDbData():
#

# get_admin_db_data:
# admin_db_data = None
# admin_id = user_id
# connect_db('our clients')
# get_raw
# admin_db_data = data_dict


# Object() - ObjectsCategories, ObjectsParts
# Database(Object)
# Table(Database)
# AdminsTable(Table)
# AdminCouponsTable(Table)
# ColNamesList(Table)
# DataDict(Table)
# (Action)

# Telegram(Object)
# Message
# Keyboard(Message)
# KeyboardType(Keyboard)
# Button(KeyboardType)
# ButtonText(Button)
# ButtonCallback(Button)
# ButtonUrl(Button)
# Text(Message)
# (Action)


# Action(User, Object) - ActionCategories
# AdminAction(Action)
# DatabaseActions(AdminAction)
# ConnectDB(AdminAction)
# GetRaw(AdminAction)
# InsertRaw(AdminAction)
# UpdateRaw(AdminAction)
# CreateTable(AdminAction)

# TelegramActions(Action)
# SendMessage(Action)


# classes
# User:
# UserAdmin,
# UserNonAdmin,
# UserTeamMember,
# UserTeamMemberRole,
# UserClient,
# SuperAdmin

# Message(User):
# AdminMessage(UserAdmin), NonAdminMessage(UserNonAdmin), UserClientMessage(UserClient)
# MessageContent(Message)
# MessageButtons(Message): WithButtons, WithBackButton, WithBackMenuButton, WithCallback, WithMainMenuButton
# MessageAction(Message, User):
# MessageActionUserInput(MessageAction)
# MessageActionSendMessage(MessageAction)

# Coupon(User):
# CouponDbData(Coupon):
# AdminCouponDbData(CouponDbData, UserAdmin)
# ClientUserCouponDbData(CouponDbData, UserClient)
# CouponStatus(ClientUserCouponDbData):
# CouponStatusActive(CouponStatus), CouponStatusNonActive(couponStatus)
# CouponParams(CouponDbData)
# CouponAction(CouponDbData):
# AdminCouponAction(CouponAction, Admin):
# ChangeCoupon(): change_name, change_cost, change_time, change_desc
# DeleteCoupon()
# AddCoupon()
# ActivateCoupon()
# UserClientCouponAction(CouponAction, UserClient)
# GetCoupon
# CouponActivatedMsg
# UseCoupon

# CouponsList(User):
# CouponsListDbData():
# AdminCouponsListDbData(CouponsListDbData, UserAdmin)
# ClientUserCouponsListDbData(CouponsListDbData, UserClient)
# CouponsListDict(CouponsList):
# AdminCouponsListDict(CouponsListDbData, UserAdmin)
# ClientUserCouponsListDict(CouponsListDbData, UserClient)
# CouponsListString(CouponsListDict):
# AdminCouponsListString(CouponsListDbData, UserAdmin)
# ClientCouponsListString(CouponsListDbData, UserClient)
# CouponsListAction(CouponsListDict):
# AdminCouponsListAction(CouponsListDbData, UserAdmin)
# ClientCouponsListAction(CouponsListDbData, UserClient)

# DataBase(User)
# DataBaseTable(DataBase, Admin):
# AdminDbData(DataBaseTable)
# AdminCouponsDbTable(DataBaseTable)
# DataBaseCols(DataBaseTable)
# DataBaseCreateTable(AdminCouponsDbTable)
# DataBaseTableConnection(DataBaseTable)
# DataBaseAction(Database):
# DataBaseActionGet(DataBaseAction):
# GetAdminData(DataBaseActionGet, Admin)
# GetCouponData(DataBaseActionGet, Admin, Coupon)
# DataBaseActionInsert(DataBaseAction)
# InsertAdminData(DataBaseActionGet, Admin)
# InsertCouponData(DataBaseActionInsert, Admin, Coupon)
# DataBaseActionUpdate(DataBaseAction)
# UpdateAdminData(DataBaseActionUpdate, Admin)
# UpdateCouponData(DataBaseActionUpdate, Admin, Coupon)
# AdminDataBaseAction(DataBaseAction):
# ClientDataBaseAction(DataBaseAction):

# Actions(User)
# MessageAction(Message):
# UserInputAction()
# SendMessage
# DataBaseAction(DataBase)
# CouponAction(Coupon)
# CouponsAction(CouponsList)
# AdminAction(UserAdmin)
# AdminSettingsAction(AdminAction)
# AdminCabinetAction(AdminAction)
# AdminPaymentAction(AdminAction)
# ClientAction(UserClient)
# UserAction(User)
