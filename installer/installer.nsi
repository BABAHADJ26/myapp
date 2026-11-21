Unicode true
!include "MUI2.nsh"
Name "قلمي"
OutFile "Qalami-Setup.exe"
InstallDir "$LOCALAPPDATA\Programs\Qalami"
RequestExecutionLevel user
SetCompressor /SOLID lzma
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_FINISHPAGE_RUN "$INSTDIR\qalami.exe"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Arabic"
VIProductVersion "1.0.0.0"
VIAddVersionKey /LANG=${LANG_ARABIC} "ProductName" "Qalami"
VIAddVersionKey /LANG=${LANG_ARABIC} "FileDescription" "Qalami setup"
VIAddVersionKey /LANG=${LANG_ARABIC} "FileVersion" "1.0.0"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "Qalami\*.*"
  File "icon.ico"
  CreateShortcut "$DESKTOP\قلمي.lnk" "$INSTDIR\qalami.exe" "" "$INSTDIR\icon.ico"
  CreateDirectory "$SMPROGRAMS\قلمي"
  CreateShortcut "$SMPROGRAMS\قلمي\قلمي.lnk" "$INSTDIR\qalami.exe" "" "$INSTDIR\icon.ico"
  WriteUninstaller "$INSTDIR\uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Qalami" "DisplayName" "قلمي"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Qalami" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Qalami" "DisplayIcon" "$INSTDIR\icon.ico"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\قلمي.lnk"
  RMDir /r "$SMPROGRAMS\قلمي"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\Qalami"
SectionEnd
