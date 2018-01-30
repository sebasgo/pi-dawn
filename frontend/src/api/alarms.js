var _alarms =[
  { id: 1, time: "09:00", enabled: true, repeat: true, repeatDays: 1+2+4+8+16 },
  { id: 2, time: "07:00", enabled: false, repeat: false, repeatDays: 0}
]

var _next_alarm_id = 3;


export default {
  getAlarms(cb) {
    setTimeout(() => cb(Array.from(_alarms)), 100)
  },
  addAlarm(data, cb) {
    setTimeout(() => {
      data.id = _next_alarm_id
      _next_alarm_id++
      _alarms.push(data)
      cb(data)
    })
  },
  updateAlarm(id, data, cb) {
    setTimeout(() => {
      for (var o of _alarms) {
        if (o.id == id) {
          Object.assign(o, data)
          cb(o)
          break
        }
      }
    }, 100)
  },
  deleteAlarm(id, cb) {
    setTimeout(() => {
      _alarms = _alarms.filter(o => o.id != id)
      cb()
    }, 100)
  }
}