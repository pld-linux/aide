Summary:	Advanced Intrusion Detection Environment
Name:		aide
Version:	0.7
Release:	1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://ftp.linux.hr/pub/aide/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Patch0:		%{name}-cvs20010627.patch.gz
URL:		http://www.cs.tut.fi/~rammer/aide.html
BuildRequires:	libgcrypt-static
BuildRequires:	gettext-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir     /etc/%{name}
%define		_pkglibdir	/var/lib/%{name}

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%description
AIDE creates a database from the regular expression rules that it
finds from the config file. Once this database is initialized it can
be used to verify the integrity of the files. It has several message
digest algorithms (md5,sha1,rmd160,tiger,haval,etc.) that are used to
check the integrity of the file. More algorithms can be added with
relative ease. All of the usual file attributes can also be checked
for inconsistencies.

%build
%configure \
	--with-config-file=%{_sysconfdir}/aide.conf \
	--with-locale \
	--without-zlib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_pkglibdir}}
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf AUTHORS ChangeLog NEWS README doc/aide.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz doc/aide.conf.gz
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/aide.conf
%attr(750,root,root) %ghost %{_pkglibdir}
%attr(755,root,root) %{_bindir}/aide
%{_mandir}/man[15]/*
