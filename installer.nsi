!define APP_NAME "CloudBase ERP"
!define EXE_NAME "CloudBase_ERP.exe"
!define INSTALLER_NAME "CloudBase_ERP_Installer.exe"
!define INSTALL_DIR "$PROGRAMFILES\\CloudBase_ERP"

OutFile "${INSTALLER_NAME}"
InstallDir ${INSTALL_DIR}
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File ".\\dist\\${EXE_NAME}"

  CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${EXE_NAME}"
  CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${EXE_NAME}"

  WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\\${EXE_NAME}"
  Delete "$INSTDIR\\Uninstall.exe"
  Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
  Delete "$DESKTOP\\${APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\\${APP_NAME}"
  RMDir "$INSTDIR"
SectionEnd
