Summary:	Advanced Intrusion Detection Environment
Summary(pl):	Zaawansowany System Wykrywania W≥amaÒ (AIDE)
Name:		aide
Version:	0.8
Release:	0.1
License:	GPL
Group:		Applications/System
Group(cs):	Aplikace/SystÈm
Group(da):	Programmer/System
Group(de):	Applikationen/System
Group(es):	Aplicaciones/Sistema
Group(fr):	Applications/SystËme
Group(is):	Forrit/Kerfisforrit
Group(it):	Applicazioni/Sistema
Group(ja):	•¢•◊•Í•±°º•∑•Á•Û/•∑•π•∆•‡
Group(no):	Applikasjoner/System
Group(pl):	Aplikacje/System
Group(pt):	AplicaÁıes/Sistema
Group(pt_BR):	AplicaÁıes/Sistema
Group(ru):	“…Ãœ÷≈Œ…—/Û…”‘≈Õ¡
Group(sl):	Programi/Sistem
Group(sv):	Till‰mpningar/System
Group(uk):	“…ÀÃ¡ƒŒ¶ “œ«“¡Õ…/Û…”‘≈Õ¡
Source0:	ftp://ftp.cs.tut.fi/pub/src/gnu/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source3:	%{name}-check
Source4:	%{name}.sysconfig
Patch2:		%{name}-autoconf.patch
URL:		http://www.cs.tut.fi/~rammer/aide.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	perl-modules
BuildRequires:	gettext-devel
BuildRequires:	glibc-static
BuildRequires:	libgcrypt-static
BuildRequires:	zlib-static
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
AIDE tworzy bazÍ danych z wyraøeÒ regularnych, ktÛre znajduj± siÍ w
pliku konfiguracyjnym. Gdy baza zostanie zainicjowana moøna sprawdzaÊ
integralno∂Ê plikÛw. Uøywanych jest kilka algorytmÛw sprawdzania
spÛjno∂ci (md5,sha1,rmd160,tiger,haval,itp.). Inne mog± byÊ dodane
stosunkowo ≥atwo. Zwyk≥e atrybuty plikÛw takøe mog± byÊ sprawdzane.

%prep
%setup -q -b 0
%patch2 -p1

%build
rm -f missing
gettextize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	--with-config-file=%{_sysconfdir}/aide.conf \
	--with-locale
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

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

#%files -f %{name}.lang
%files
%defattr(644,root,root,755)
%doc *.gz doc/aide.conf.gz doc/manual.html
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/aide.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/aide
%attr(750,root,root) %dir %{_pkglibdir}
%attr(755,root,root) %{_bindir}/aide
%attr(700,root,root) %config(noreplace) /etc/cron.daily/aide-check
%{_mandir}/man[15]/*
#%lang(ru) %{_mandir}/ru/man[15]/*
