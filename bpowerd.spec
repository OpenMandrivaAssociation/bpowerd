%define name bpowerd
%define version 3.0b1
%define release %mkrel 10

Summary: Power Control Program for Best Patriot UPS
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
URL: https://www.ccraig.org/bpowerd/ 
Group: Monitoring
Source: %name-%version.tar.bz2
Source1: bpowerd
Source2: power
Source3: INSTALL
Requires: SysVinit >= 2.64, initscripts, chkconfig
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
A program that monitors Best Patriot UPS systems for power outages
and alarms and calls init when they occur.  Allows for the automated
shutdown of the system when alarms occur and killing of the inverter
on shutdown.

%prep

%setup -q
# specifying --with-shutdown allows configure to be run as non-root
CFLAGS="$RPM_OPT_FLAGS" ./configure --with-shutdown=/var/run/shutdown.pid

%build
%make

%install
rm -rf $RPM_BUILD_ROOT

install -m 755 -d $RPM_BUILD_ROOT%{_sbindir}
install -m 755 -s bpowerd $RPM_BUILD_ROOT%{_sbindir}/bpowerd

install -m 755 -d $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 bpowerd.man $RPM_BUILD_ROOT%{_mandir}/man8/

install -d  $RPM_BUILD_ROOT/etc/rc.d/init.d
install  -m 755 bpowerfail $RPM_BUILD_ROOT/etc/rc.d/init.d/bpowerfail
install  -m 755 ${RPM_SOURCE_DIR}/bpowerd $RPM_BUILD_ROOT/etc/rc.d/init.d/bpowerd

install -d  $RPM_BUILD_ROOT/etc/sysconfig
install -m 644 ${RPM_SOURCE_DIR}/power $RPM_BUILD_ROOT/etc/sysconfig/power
install -m 644 ${RPM_SOURCE_DIR}/INSTALL INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_sbindir}/*
%config(noreplace) /etc/rc.d/init.d/bpowerfail
%config(noreplace) /etc/rc.d/init.d/bpowerd
%{_mandir}/man8/*
%config(noreplace) /etc/sysconfig/power
%defattr(0644,root,root,755)
%doc README INSTALL

%post
/sbin/chkconfig --add bpowerd
echo "Please read /usr/doc/bpowerd-%{PACKAGE_VERSION}/INSTALL for info on configuring bpowerd"
echo "This is mandatory as bpowerd will not run as currently configured"

%postun
/sbin/chkconfig --del bpowerd

