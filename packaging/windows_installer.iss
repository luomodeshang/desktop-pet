; ============================================
; 桌面宠物程序 - Inno Setup安装脚本
; 创建真正的Windows安装程序
; ============================================

#define MyAppName "桌面宠物程序"
#define MyAppVersion "1.0.5"
#define MyAppPublisher "luomodeshang"
#define MyAppURL "https://github.com/luomodeshang/desktop-pet"
#define MyAppExeName "DesktopPet.exe"

[Setup]
AppId={{D3C8A4B1-9E2F-4A7C-B8D3-123456789ABC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=USER_GUIDE_小白版.md
OutputDir=dist
OutputBaseFilename=DesktopPet_Setup
SetupIconFile=assets\images\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
; 主程序文件（需要手动替换为实际的EXE）
Source: "dist\DesktopPet.exe"; DestDir: "{app}"; Flags: ignoreversion
; 配置文件
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs
; 资源文件
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
; 文档文件
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_GUIDE_小白版.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "WINDOWS_USER_GUIDE_EXE.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "Windows_用户助手.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // 安装完成后显示说明
    MsgBox('安装完成！' + #13#10 + #13#10 +
           '使用说明：' + #13#10 +
           '1. 首次运行需要选择一张照片' + #13#10 +
           '2. 左键点击宠物：触发动作' + #13#10 +
           '3. 右键点击宠物：投喂食物' + #13#10 +
           '4. 拖动宠物：移动位置' + #13#10 + #13#10 +
           '杀毒软件可能误报，请点击"仍要运行"',
           mbInformation, MB_OK);
  end;
end;