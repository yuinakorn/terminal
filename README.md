## ติดตั้ง virtualbox

https://www.virtualbox.org/

เซ็ต network ให้เป็น bridge เพื่อให้เราสามารถเข้าถึงเครื่องจำลองได้

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


```bash
yum install mariadb-server mariadb-devel mariadb-test mariadb-backup -y
```

**รันทีละคำสั่ง**

```bash
sudo systemctl start mariadb
sudo systemctl status mariadb
sudo systemctl enable mariadb
```

**เช็ค version**

```bash
mysql --version
```

**ตั้งค่า mysql secure**

```bash
sudo mysql_secure_installation
```

```bash
Enter current password for root (enter for none):
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n] n
 ... skipping.

By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] y
 ... Success!

By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] y
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.

Thanks for using MariaDB!
```

เข้าไปใน mysql สร้าง user "adminit" 

```bash
mysql -u root -p
```


```bash
CREATE USER 'adminit'@'%' IDENTIFIED BY '123456';
```

```bash
GRANT ALL PRIVILEGES ON *.* TO 'adminit'@'%' WITH GRANT OPTION;

FLUSH PRIVILEGES;
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

**เช็ค package ที่ติดตั้งแล้ว**
```bash
pip3.9 freeze
```

