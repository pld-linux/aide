Summary:	Advanced Intrusion Detection Environment
Summary(pl):	Zaawansowany System Wykrywania W³amañ (AIDE)
Name:		aide
Version:	0.8
Release:	2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.cs.tut.fi/pub/src/gnu/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}-0.7-doc.tar.bz2
Source3:	%{name}-check
Source4:	%{name}.sysconfig
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-NLS.patch
URL:		http://www.cs.tut.fi/~rammer/aide.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	findutils
BuildRequires:	bison
BuildRequires:	perl-modules
BuildRequires:	gettext-devel
BuildRequires:	glibc-static
BuildRequires:	libgcrypt-static
BuildRequires:	zlib-static >= 1.1.4
Requires:	crondaemon
Requires:	mailx
Requires:	grep
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir     /etc/%{name}
%define		_pkglibdir	/var/lib/%{name}

%description
AIDE creates a database from the regular expression rules that it
finds from the config file. Once this database is initialized it can
be used to verify the integrity of the files. It has several message
digest algorithms (md5,sha1,rmd160,tiger,haval,etc.) that are used to
check the integrity of the file. More algorithms can be added with
relative ease. All of the usual file attributes can also be checked
for inconsistencies.

%description -l pl
AIDE tworzy bazê danych z wyra¿eñ regularnych, które znajduj± siê w
pliku konfiguracyjnym. Gdy baza zostanie zainicjowana mo¿na sprawdzaæ
integralno¶æ plików. U¿ywanych jest kilka algorytmów sprawdzania
spójno¶ci (md5,sha1,rmd160,tiger,haval,itp.). Inne mog± byæ dodane
stosunkowo ³atwo. Zwyk³e atrybuty plików tak¿e mog± byæ sprawdzane.

%prep
%setup -q -b 0 -a 2
%patch0 -p1
%patch1 -p1

%build
rm -f missing po/Makefile*
find . -name "*.c" -type f > po/POTFILES.in
gettextize --copy --force
aclocal
autoconf
automake -a -c -f
%configure \
	--with-config-file=%{_sysconfdir}/aide.conf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pkglibdir},/etc/cron.daily,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/aide

gzip -9nf AUTHORS ChangeLog NEWS README doc/aide.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz doc/aide.conf.gz doc/manual.html aide-*/doc/aide.html
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/aide.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/aide
%attr(750,root,root) %dir %{_pkglibdir}
%attr(755,root,root) %{_bindir}/aide
%attr(700,root,root) %config(noreplace) /etc/cron.daily/aide-check
%{_mandir}/man[15]/*
