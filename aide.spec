Summary:	Advanced Intrusion Detection Environment
Name:		aide
Version:	20010624
Release:	0.1
License:	GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
#Source0:	ftp://ftp.linux.hr/pub/aide/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
URL:		http://www.cs.tut.fi/~rammer/aide.html
#Source1:	%{name}.conf
BuildRequires:	libgcrypt-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/%{name}

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p1

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
	--without-zlib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
#%config(noreplace) %{_sysconfdir}/aide.conf
%attr(755,root,root) %{_bindir}/aide
%{_mandir}/man[15]/*
