import logging
import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from configs import config


define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ("/iap", IAPHandler),
            ("/guestLogin", GuestLoginHandler),
            ("/getChannelConfig", ChannelConfigHandler),
            ("/refreshToken", RefreshHandler),
            ("/createRoom", CreateRoomHandler),
            ("/getOpenRoomInfo", OpenRoomInfoHandler),
            ("/getDiamondsChange", DiamondsHandler),
            ("/queryServerInfo", QueryRoomHandler),
            ("/getRoomList", PlayRoomListHandler),
            ("/getRoundList", RoundListHandler),
            ("/uploadAAC", UploadAACHandler),
            ("/fetchAAC/(\w+)", GetAACHandler),
            ("/checkUpdate", CheckUpdateHandler),
            ("/wechatLogin", WeChatLoginHandler),
            ("/getAgentRoomList", GetAgentRoomList),

            ("/queryUid", QueryUidHandler),
            ("/xianliaoLogin", XianLiaoLoginHandler),

            ("/getDiamondRecords", DiamondRecordsHandler),
            ("/giveDiamonds", GiveDiamondsHandler),
            ("/editProfiles", EditProfileHandler),
            ("/resetPwd", ResetPwdHandler),
            ("/requestVerifyCode", RequestVerifyCodeHandler),

            ("/makeReviewCode", MakeReviewCodeHandler),
            ("/getRoundInfo", GetByReviewCodeHandler),
            ("/getRoundPlayDetail", RePlayDetailsHandler),

            ("/getRoundRank", RoundRankHandler),
            ("/saveMobilePhone", SetPhoneHandler),
            ("/uploadGeo", UploadGeoHandler),
            ("/shareDiamond", ShareDiamondHandler),
            ("/loginDiamond", LoginDiamondHandler),
            ("/shareDiamondEveryDay", ShareDiamondEveryDayHandler),

            ("/createClub", CreateClubHandler),
            ("/getClubs", GetClubHandler),
            ("/copyClub", CopyClubHandler),
            ("/editClubNotice", UpdateClubNoticeHandler),
            ("/editClubName", UpdateClubNameHandler),
            ("/joinClub", ApplyClubHandler),
            ("/addPlayerToClub", AgreeClubHandler),
            ("/getRequestJoinList", GetVerifyListClubHandler),
            ("/verifyClubUser", VerifyClubUserHandler),
            ("/clubUserList", GetClubUserHandler),
            ("/kickClubUser", KickUserHandler),
            ("/setPlayerPermission", SetUserPermission),
            ("/remarkClubUser", SetUserRemark),
            ("/dismissClub", DismissClubHandler),
            ("/upgradeClub", UpgradeClubHandler),
            ("/getClubConfig", GetClubConfig),

            ("/getDetailsResult", GetDetailsResultHandler),
            ("/getClubScoreList", GetClubScoreListHandler),
            ("/getClubScoreListByGameTypeAndTime", GetClubScoreListByGameTypeAndTime),
            ("/getClubInfo", GetClubInfoHandler),
            ("/getClubOwnerInfo", GetClubOwnerInfo),
            ("/getClubDiamondInfo", GetClubDiamondInfo),
            ("/setClubAutoRoom", SetClubAutoRoomHandler),
            ("/setClubMode", SetClubModeHandler),
            ("/getClubRooms", GetClubRoomHandler),
            ("/getClubRoomsByMatchType", GetClubRoomByMatchTypeHandler),
            ("/getRobotRooms", RobotRoomsHandler),
            ("/clubsRoomRank", ClubsDataHandler),
            # ("/getClubOwnerRoomInfo", GetClubOwnerRoomInfo),
            ("/clubQuickRoom", GetClubQuickRoom),
            ("/getClubScoreByUid", GetClubScoreByUid),
            ("/getClubWinnerList", GetClubWinnerList),
            ("/setClubWinnerList", SetClubWinnerList),
            ("/getClubWinnerRank", GetClubWinnerRank),
            ("/transferClub", TransferClub),

            ("/inviteFriendList", InviteFriendListHandler),
            ("/withdrawRecords", WithdrawRecordsHandler),
            ("/getInviteActivityConfig", InviteActivityConfigHandler),
            ("/exchange", ExchangeHandler),
            ("/withdraw", WithdrawHandler),
            ("/shareInvite", ShareInviteHandler),
            ("/clubShare", ClubShareHandler),
            ("/clubShare.json", ClubShareHandler),

            ("/shop", DiamondPriceHandler),
            ("/feedBack", FeedBackHandler),

            ("/quitClub", QuitClubHandler),
            ("/bindInvite", BindHandler),
            ("/wxpay", WechatPayHandler),
            ("/clubUserRank", GetClubUserRank),
            ("/dumpRecord", DumpRecordHandler),

            ("/increaseDou", IncreaseDou),
            ("/reduceDou", ReduceDou),
            ("/queryDou", QueryDou),
            ("/queryDouLogs", QueryDouLogs),
            ("/queryDouOperLogs", QueryDouOperLogs),

            ("/getFloor", GetFloorHandler),
            ("/addFloor", AddFloorHandler),
            ("/editFloor", EditFloorHandler),
            ("/delFloor", DelFloorHandler),

            ("/getSubFloor", GetSubFloorHandler),
            ("/getSubFloorByMatchType", GetSubFloorByMatchTypeHandler),
            ("/addSubFloor", AddSubFloorHandler),
            ("/editSubFloor", EditSubFloorHandler),
            ("/delSubFloor", DelSubFloorHandler),

            ("/clubDouLogs", ClubDouLogs),
            ("/clubUserDouLogs", ClubUserDouLogs),
            ("/clubUserDetailDouLogs", ClubUserDetailDouLogs),
            ("/qrcode", QRCodeHandler),

            ("/recharge", RechargeConfig),
            ("/modifyAddress", ModifyAddressHandler),
            ("/getAddress", GetAddressHandler),
            ("/buyScoreItem", BuyScoreItemHandler),

            ("/signInActivity", SignInActivity),
            ("/signInItemInfo", SignInItemInfo),
            ("/checkRoom", CheckRoomHandler),

            ("/getGameCountLogs", GetGameCountLogs),
            ("/setGameCountLogs", SetGameCountLogs),

            ("/setClubBlock", SetClubBlockHandler),
            ("/getClubGamePlay", GetClubGamePlay),
            ("/queryClubBlock", QueryClubBlockHandler),
            ("/getClubUserRoomInfo", GetClubUserRoomInfo),

            ("/transferClubUser", TransferClubUser),
            ("/getClubBaseInfo", GetClubBaseInfo),
            ("/tagClubUser", TagClubUser),
            ("/getClubTagUserRoomInfo", GetClubTagUserRoomInfo),
            ("/getClubGameLogs", GetClubGameLogs),
            ("/getClubRoomList", PlayRoomListWithClubAndTimeHandler),

            ("/setClubQueryWinnerScore", SetClubQueryWinnerScore),

            ("/getClubTask", GetClubTask),
            ("/modifyClubTask", ModifyClubTask),
            ("/taskClubShare", TaskClubShare),
            ("/bonusClubTaskShare", BonusClubTaskShare),
            ("/bonusClubTaskRound", BonusClubTaskRound),

            ("/changeYuanBaoToDiamond", ChangeYuanBaoToDiamond),
            ("/buyYuanBaoHandler", BuyYuanBaoHandler),

            ("/springActivity", SpringActivity),
            ("/springActivityRecv", SpringActivityRecv),
            ("/springActivityLogs", SpringActivityLogs),

            ("/suspendClubUser", SuspendClubUserHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=config.static_path,
            xsrf_cookies=False,
            debug=config.IS_DEBUG,
            xheaders=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


# Web Server 实例
server = None


def main():
    global server
    logging.basicConfig(filename=config.LOG_PATH + 'run.txt', level=logging.DEBUG)
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit')


if __name__ == "__main__":
    main()
