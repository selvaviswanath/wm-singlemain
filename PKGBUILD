pkgname=mytilingwm
pkgver=1.0
pkgrel=1
pkgdesc="My tiling window manager"
arch=('i686' 'x86_64')
url="https://github.com/selvaviswanath/wm-singlemain"
license=('MIT')
depends=('python-xlib' 'wmctrl')
source=("https://github.com/selvaviswanath/wm-singlemain/archive/main.zip")
sha256sums=('put-the-sha256-hash-of-the-zip-file-here')

build() {
    cd "$srcdir/mytilingwm-main"
    python setup.py build
}

package() {
    cd "$srcdir/mytilingwm-main"
    python setup.py install --root="$pkgdir/" --optimize=1
}
