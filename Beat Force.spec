# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/Samar Syed/Desktop/Beat Force App Exe/src/MapGeneration.py'],
             pathex=['C:\\Users\\Samar Syed\\Desktop\\Beat Force App Exe\\src'],
             binaries=[],
             datas=[('C:\\ProgramData\\Anaconda3\\envs\\beatforce\\lib\\site-packages\\eel\\eel.js', 'eel'), ('web', 'web'), ('C:/Users/Samar Syed/Desktop/Beat Force App Exe/src/HMM_modeling.py', '.'), ('C:/Users/Samar Syed/Desktop/Beat Force App Exe/src/models', 'models/'), ('C:/Users/Samar Syed/Desktop/Beat Force App Exe/src/envs', 'envs/'), ('C:/Users/Samar Syed/Desktop/Beat Force App Exe/src/web', 'web/'), ('C:/Users/Samar Syed/Desktop/Beat Force App Exe/src/cover.jpg', '.')],
             hiddenimports=['bottle_websocket', 'librosa', 'markovify'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Beat Force',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\Samar Syed\\Desktop\\Beat Force App Exe\\src\\beatforce.ico')
