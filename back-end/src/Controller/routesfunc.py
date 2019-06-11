from Model.basic import check
from Object.params import check
from Object.user import user
from Object.point import point, points


def connect(cn, nextc):
    err = check.contain(cn.pr, ["mail", ["password", "token"]])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]

    use = user(cn.pr["mail"], cn.pr["password"], cn.pr["token"])
    err = use.connect()
    cn.private["user_id"] = use.id
    return cn.call_next(nextc, err)

def register(cn, nextc):
    err = check.contain(cn.pr, ["mail", "password", "password2"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    use = user(cn.pr["mail"], cn.pr["password"])
    err = use.register(cn.pr["password2"])
    return cn.call_next(nextc, err)

def addpoint(cn, nextc):
    err = check.contain(cn.pr, ["key", "sig_id"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    cn.pr = err[1]
    device = point(None, cn.private["user_id"], cn.pr["key"], cn.pr["sig_id"])
    err = device.infos()
    return cn.call_next(nextc, err)

def infos(cn, nextc):
    err = check.contain(cn.pr, ["point_id"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    device = point(cn.pr["point_id"], cn.private["user_id"])
    err = device.infos()
    return cn.call_next(nextc, err)

def share(cn, nextc):
    err = check.contain(cn.pr, ["point_id", "mail_to"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    device = point(cn.pr["point_id"], cn.private["user_id"])
    err = device.share(cn.pr["mail_to"])
    return cn.call_next(nextc, err)

def surname(cn, nextc):
    err = check.contain(cn.pr, ["point_id", "surname"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    device = point(cn.pr["point_id"], cn.private["user_id"])
    err = device.rename(cn.pr["surname"])
    return cn.call_next(nextc, err)

def getall(cn, nextc):
    devices = points(cn.private["user_id"])
    err = devices.getall()
    return cn.call_next(nextc, err)

def getalldetails(cn, nextc):
    devices = points(cn.private["user_id"])
    err = devices.getalldetails()
    return cn.call_next(nextc, err)
