เตรียม terminal ก่อน 
ติดตั้ง zsh

install ohmyz.sh
[Oh My Zsh - a delightful & open source framework for Zsh](https://ohmyz.sh/#install)

```bash
yum install zsh
```

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
```

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
```


```bash
nano ~/.zshrc
```

หาบรรทัดโค้ดตามนี้ และ ลบ # ออก ก็ถือว่าเราเปิดใช้ ( ลบ comment )
```bash
ENABLE_CORRECTION="true"
```

```bash
plugins=(git
zsh-autosuggestions
zsh-syntax-highlighting
)
```


#ธีมนี้สวย
ZSH_THEME="agnoster"
ธีมเพิ่มเติม
https://github.com/ohmyzsh/ohmyzsh/wiki/Themes

#หาติดตั้งเพิ่มได้
ZSH_THEME="powerlevel10k/powerlevel10k"
วีธีเปลี่ยน style อีกครั้ง
p10k configure