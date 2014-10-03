Summary:	A simple lightweight powerful embeddable programming language
Name:		lua
Version:	5.1.5
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	http://www.lua.org/ftp/lua-%{version}.tar.gz
# Source0-md5:	2e115fe26e435e33b0d5c022e4490567
Patch0:		%{name}-link.patch
URL:		http://www.lua.org/
BuildRequires:	readline-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lua is a powerful, light-weight programming language designed for
extending applications. It is also frequently used as a
general-purpose, stand-alone language. It combines simple procedural
syntax (similar to Pascal) with powerful data description constructs
based on associative arrays and extensible semantics. Lua is
dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package libs
Summary:	lua libraries
Group:		Development/Languages

%description libs
lua libraries.

%package devel
Summary:	Header files for Lua
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files needed to embed Lua in C/C++ programs and docs for the
language.

%prep
%setup -q
%patch0 -p1

%{__sed} -r -i 's|(#define LUA_ROOT.*)%{_prefix}/local/|\1%{_prefix}/|g' src/luaconf.h
%{__sed} -r -i 's|(#define LUA_CDIR.*)lib/|\1%{_lib}/|g' src/luaconf.h

%build
%{__make} all \
	PLAT=linux	\
	CC="%{__cc}"	\
	CFLAGS="%{rpmcflags} -Wall -fPIC -DPIC -D_GNU_SOURCE -DLUA_USE_LINUX"	\
	OPTLDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/lua

%{__make} install \
	INSTALL_MAN=$RPM_BUILD_ROOT%{_mandir}/man1	\
	INSTALL_TOP=$RPM_BUILD_ROOT%{_prefix}		\
	INSTALL_CMOD=$RPM_BUILD_ROOT%{_libdir}/lua/5.1

install src/liblua.so.5.1 $RPM_BUILD_ROOT%{_libdir}
ln -s liblua.so.5.1 $RPM_BUILD_ROOT%{_libdir}/liblua.so

# create pkgconfig file
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
cat > $RPM_BUILD_ROOT%{_pkgconfigdir}/lua.pc <<'EOF'
compiler=%{_bindir}/luac
exec_prefix=%{_exec_prefix}
includedir=%{_includedir}
interpreter=%{_bindir}/lua
libdir=%{_libdir}
prefix=%{_prefix}

Name: Lua
Description: An extension programming language
Version: %{version}
Cflags: -I%{_includedir}/%{name}
Libs: -L%{_libdir} -llua -ldl -lm
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lua
%attr(755,root,root) %{_bindir}/luac
%{_mandir}/man1/lua.1*
%{_mandir}/man1/luac.1*

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT HISTORY README
%attr(755,root,root) %{_libdir}/liblua.so.*.*
%dir %{_datadir}/lua
%dir %{_libdir}/lua
%{_datadir}/lua/5.1
%{_libdir}/lua/5.1

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,css,gif} test
%attr(755,root,root) %{_libdir}/liblua.so
%{_includedir}/*.h
%{_includedir}/*.hpp
%{_pkgconfigdir}/lua.pc

