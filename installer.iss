[Setup]
AppName=Vision Inspect
AppVersion=1.0
DefaultDirName={pf}\VisionInspect
DefaultGroupName=VisionInspect

; 🔥 Optimization
Compression=lzma2
SolidCompression=yes
CompressionThreads=auto
DiskSpanning=no

; 🔐 Better UX
WizardStyle=modern
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\vision-inspect.exe

OutputDir=installer
OutputBaseFilename=vision-inspect-setup

[Files]
Source: "vision-inspect.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Vision Inspect"; Filename: "{app}\vision-inspect.exe"

[Run]
Filename: "{app}\vision-inspect.exe"; Description: "Launch App"; Flags: nowait postinstall skipifsilent