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

; 🔐 Optional UI (safe fallback)
SetupIconFile=storage\icon.ico
WizardStyle=modern
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\vision-inspect.exe

OutputDir=installer
OutputBaseFilename=vision-inspect-setup

; 🔐 Required for Program Files install
PrivilegesRequired=admin

[Files]
Source: "dist\vision-inspect.exe"; DestDir: "{app}"; Flags: ignoreversion

; Only include .env if exists
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\Vision Inspect"; Filename: "{app}\vision-inspect.exe"

[Run]
Filename: "{app}\vision-inspect.exe"; Description: "Launch App"; Flags: nowait postinstall skipifsilent