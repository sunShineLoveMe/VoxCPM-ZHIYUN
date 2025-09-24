#!/usr/bin/env python3
"""
VoxCPM 模型下载修复脚本
解决 config.json 文件缺失问题
"""

import os
import sys

def download_voxcpm_model():
    """下载 VoxCPM 模型文件"""
    try:
        from huggingface_hub import snapshot_download
        
        # 设置模型目录
        model_dir = "models/openbmb__VoxCPM-0.5B"
        
        # 确保目录存在
        os.makedirs(model_dir, exist_ok=True)
        
        print(f"🚀 开始下载 VoxCPM-0.5B 模型到 {model_dir}")
        print("⏳ 这可能需要几分钟时间，请耐心等待...")
        
        # 从 HuggingFace 下载模型
        snapshot_download(
            repo_id="openbmb/VoxCPM-0.5B",
            local_dir=model_dir,
            local_dir_use_symlinks=False,
            resume_download=True,
            ignore_patterns=["*.git*", "README.md"]
        )
        
        print("✅ 模型下载完成！")
        
        # 验证关键文件是否存在
        required_files = ["config.json", "pytorch_model.bin"]
        for file in required_files:
            file_path = os.path.join(model_dir, file)
            if os.path.exists(file_path):
                print(f"✅ {file} 文件存在")
            else:
                print(f"❌ {file} 文件缺失")
                return False
        
        return True
        
    except ImportError:
        print("❌ 缺少 huggingface_hub 依赖")
        print("请安装: pip install huggingface_hub")
        return False
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False

def check_existing_model():
    """检查现有模型文件"""
    model_dirs = [
        "models/VoxCPM-0.5B",  # 默认目录
        "models/openbmb__VoxCPM-0.5B",  # HF格式目录
    ]
    
    for model_dir in model_dirs:
        config_path = os.path.join(model_dir, "config.json")
        if os.path.exists(config_path):
            print(f"✅ 找到现有模型: {model_dir}")
            return model_dir
    
    return None

def fix_app_py_model_path():
    """修复 app.py 中的模型路径配置"""
    app_py_path = "app.py"
    
    if not os.path.exists(app_py_path):
        print("❌ 找不到 app.py 文件")
        return False
    
    # 读取文件内容
    with open(app_py_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改默认模型路径
    old_path = './models/VoxCPM-0.5B'
    new_path = './models/openbmb__VoxCPM-0.5B'
    
    if old_path in content:
        content = content.replace(old_path, new_path)
        
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 app.py 中的模型路径: {old_path} -> {new_path}")
        return True
    else:
        print("ℹ️  app.py 中的模型路径已经正确")
        return True

def main():
    """主函数"""
    print("🔧 VoxCPM 模型修复工具")
    print("=" * 50)
    
    # 检查现有模型
    existing_model = check_existing_model()
    
    if existing_model:
        print(f"✅ 找到现有模型: {existing_model}")
        # 如果模型在默认位置，更新app.py路径
        if existing_model == "models/VoxCPM-0.5B":
            fix_app_py_model_path()
    else:
        print("📥 未找到模型文件，开始下载...")
        if download_voxcpm_model():
            print("🎉 模型下载并配置完成！")
        else:
            print("❌ 模型下载失败")
            sys.exit(1)
    
    # 验证最终配置
    print("\n🔍 验证配置...")
    model_dir = "models/openbmb__VoxCPM-0.5B"
    config_path = os.path.join(model_dir, "config.json")
    
    if os.path.exists(config_path):
        print("✅ 配置验证成功！可以运行 python app.py")
    else:
        print("❌ 配置验证失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
