; 桌面宠物程序 - Inno Setup 安装脚本
; 编译前请确保已安装 Inno Setup: https://jrsoftware.org/isdl.php

#define MyAppName "桌面宠物程序"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "luomodeshang"
#define MyAppURL "https://github.com/luomodeshang/desktop-pet"
#define MyAppExeName "DesktopPet.exe"
#define MyAppAssocName MyAppName + " 文件"
#define MyAppAssocExt ".deskpet"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; 注意: AppId 的值在每次发布新版本时不要更改
AppId={{D3C8A4B1-9E2F-4A7C-B8D3-123456789ABC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=LICENSE.txt
; 如果不需要卸载密码，移除下面一行
; UninstallPassword=123456
; 压缩方式
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
; 安装程序图标
SetupIconFile=assets\images\icon.ico
; 输出文件名
OutputBaseFilename=DesktopPet_Setup
; 输出目录
OutputDir=dist
; 安装程序大小
DiskSpanning=no

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 主程序文件
Source: "dist\DesktopPet.exe"; DestDir: "{app}"; Flags: ignoreversion
; 配置文件
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
; 资源文件
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; 许可证文件
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
; 用户指南
Source: "USER_GUIDE_小白版.md"; DestDir: "{app}"; Flags: ignoreversion
; 如果需要，可以包含Python运行环境
; Source: "python_runtime\*"; DestDir: "{app}\python_runtime"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
; 注册文件关联（可选）
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocName}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocName}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocName}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
; 添加到卸载程序列表
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "DisplayName"; ValueData: "{#MyAppName}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "Publisher"; ValueData: "{#MyAppPublisher}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "URLInfoAbout"; ValueData: "{#MyAppURL}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "UninstallString"; ValueData: """{uninstallexe}"""; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: dword; ValueName: "NoModify"; ValueData: 1; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: dword; ValueName: "NoRepair"; ValueData: 1; Flags: uninsdeletekey

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; 安装完成后运行程序
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
; 显示用户指南
Filename: "{app}\USER_GUIDE_小白版.md"; Description: "查看使用指南"; Flags: shellexec postinstall skipifsilent unchecked

[Code]
// 自定义安装页面
procedure InitializeWizard;
begin
  // 添加自定义页面（可选）
end;

// 安装前检查
function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // 检查是否已安装旧版本
  if RegKeyExists(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}') then
  begin
    if MsgBox('检测到已安装旧版本，是否继续安装？', mbConfirmation, MB_YESNO) = IDNO then
      Result := False;
  end;
  
  // 检查磁盘空间（至少需要200MB）
  if DiskSpaceFunc(ExpandConstant('{app}')) < 200 then
  begin
    MsgBox('磁盘空间不足，请清理至少200MB空间。', mbError, MB_OK);
    Result := False;
  end;
end;

// 安装后操作
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 创建数据目录
    ForceDirectories(ExpandConstant('{userappdata}\{#MyAppName}\data'));
    
    // 复制示例照片（可选）
    // FileCopy(ExpandConstant('{app}\assets\images\sample.jpg'), 
    //          ExpandConstant('{userappdata}\{#MyAppName}\data\sample.jpg'), False);
  end;
end;

// 卸载前操作
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // 询问是否保留用户数据
    if MsgBox('是否保留您的宠物数据和设置？', mbConfirmation, MB_YESNO) = IDNO then
    begin
      // 删除用户数据
      DelTree(ExpandConstant('{userappdata}\{#MyAppName}'), True, True, True);
    end;
  end;
end;