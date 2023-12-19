## ติดตั้ง virtualbox

https://www.virtualbox.org/

## ติดตั้ง Oracle Linux 8.9


---


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

---

## ติดตั้ง mariadb

a) Add the MariaDB Yum Repository:

There are two ways to do this:

Using the MariaDB Package Repository Setup Script:
Download the script:
```bash 
wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
```

Make it executable:
```bash 
chmod +x mariadb_repo_setup
```
Run the script, specifying the desired MariaDB version (10.1.48 in your case):
```bash
./mariadb_repo_setup --mariadb-server-version=10.1.48
```
Manually configuring the repository:
Create a file named /etc/yum.repos.d/mariadb.repo with the following content:

```bash
[mariadb]
name=MariaDB 10.1 Repository
baseurl=https://yum.mariadb.com/10.1/linux-x86_64/
gpgkey=https://yum.mariadb.com/MariaDB-GPG-KEY
gpgcheck=yes
enabled=yes

[mariadb-10.1-compat]
name=MariaDB 10.1 Compatibility Repository
baseurl=https://yum.mariadb.com/10.1/compat-linux-x86_64/
gpgkey=https://yum.mariadb.com/MariaDB-GPG-KEY
gpgcheck=yes
enabled=yes
```

b) Install MariaDB:

Update your package list:
```bash 
sudo dnf update
```
Install the MariaDB server package:
```bash
sudo dnf install mariadb-server
```

```bash
yum install mariadb-server mariadb-devel mariadb-test mariadb-backup
```

## ติดตั้ง python3.9


```bash
sudo dnf module install python39
```

```bash
python3.9 --version
```

### ติดตั้ง progressbar2 และ mysql-connector ของ python3.9

```bash
pip3.9 install progressbar2 mysql-connector
```
