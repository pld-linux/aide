Summary:	Advanced Intrusion Detection Environment
Name:		aide
Version:	20010624
Release:	0.1
URL:		http://www.cs.tut.fi/~rammer/aide.html
Source0:	%{name}-%{version}.tar.gz
#Source1:	%{name}.conf
License:	GPL
Group:		Console/Security
Provides:	aide
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

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aide
%{_mandir}/man[15]/*
#%config(noreplace) %{_sysconfdir}/aide.conf
#%doc

%clean
#rm -rf $RPM_BUILD_ROOT
