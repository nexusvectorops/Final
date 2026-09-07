[app]
title = System Update
package.name = com.android.systemupdate
package.domain = org.android
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,java
version = 1.0
requirements = python3,kivy,requests,urllib3,pyjnius
orientation = portrait
fullscreen = 1
hide_navigation_bar = 1
hide_status_bar = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE
android.api = 30
android.minapi = 21
android.gradle_dependencies = implementation 'androidx.core:core:1.6.0'
android.arch = arm64‑v8a,armeabi‑v7a
p4a.branch = master
android.add_src = service/ServiceMyservice.java
android.allow_backup = false
android.debuggable = false
android.entrypoint = org.kivy.android.PythonActivity
android.service = org.myserviceapp.myserviceapp.ServiceMyservice
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

[buildozer]
log_level = 2
warn_on_root = 0
