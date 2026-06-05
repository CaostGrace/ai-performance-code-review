# 后台、电量与系统合规

> §9.7 后台、电量与系统合规。规则 ID 前缀 `BG-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| BG-01 | P0 | 后台任务使用合规 API | ```kotlin
// ❌ 滥用隐式广播 + 常驻服务
class MyReceiver : BroadcastReceiver() { ... }
// Manifest: <receiver android:exported="true"> <intent-filter> <action android:name="android.intent.action.TIME_TICK"/>
``` | ```kotlin
// ✅ WorkManager
val request = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES).build()
WorkManager.getInstance(ctx).enqueue(request)
``` | 系统杀进程 | 官方后台限制文档 |
| BG-02 | P1 | WakeLock/定位/传感器及时释放 | ```kotlin
// ❌ 长时间持有 WakeLock
val wl = pm.newWakeLock(PARTIAL_WAKE_LOCK, "tag")
wl.acquire(10 * 60 * 1000) // 10 分钟!
``` | ```kotlin
// ✅ 用完即释放
wl.acquire(30 * 1000)
try { doWork() } finally { wl.release() }
``` | Battery Historian 异常 | Battery Historian |
| BG-03 | P1 | 精确定时与轮询 | ```kotlin
// ❌ 高频 Alarm
val alarm = AlarmManager()
alarm.setRepeating(RTC, 0, 60 * 1000, pendingIntent)
``` | ```kotlin
// ✅ JobScheduler 约束
val builder = JobInfo.Builder(1, ComponentName(ctx, Job::class.java))
    .setMinimumLatency(15 * 60 * 1000)
    .setRequiredNetworkType(NETWORK_TYPE_UNMETERED)
``` | 待机耗电高 | Battery Historian |
| BG-04 | P2 | 推送与拉取策略 | ```kotlin
// ❌ 无条件全量拉
fun onMessage(msg: RemoteMessage) { syncAll() }
``` | ```kotlin
// ✅ 增量 + Doze 兼容
fun onMessage(msg: RemoteMessage) { syncDelta(msg.since) }
``` | 后台流量大 | — |
| BG-05 | P0 | Android 14+ 前台服务须声明类型 | ```kotlin
// ❌ 未声明 foregroundServiceType
startForeground(NOTIFICATION_ID, notification)
``` | ```kotlin
// ✅ Manifest 声明
<service android:foregroundServiceType="dataSync|location" />
startForeground(NOTIFICATION_ID, notification, FOREGROUND_SERVICE_TYPE_DATA_SYNC)
``` | 系统拒绝启动 | 官方前台服务文档 |
| BG-06 | P1 | 精确闹钟权限适配（Android 12+） | ```kotlin
// ❌ 无权限检查
alarmMgr.setExactAlarm(RTC_WAKEUP, time, pi)
``` | ```kotlin
// ✅ 前置检查
if (alarmMgr.canScheduleExactAlarms()) {
    alarmMgr.setExactAlarm(RTC_WAKEUP, time, pi)
} else {
    alarmMgr.setWindow(RTC_WAKEUP, time, 60*1000, pi)
}
``` | 闹钟静默失败 | 官方文档 |
