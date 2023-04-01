#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	tests		# integration tests
#
Summary:	Attest the trustworthiness of a device against a human using time-based one-time passwords
Summary(pl.UTF-8):	Poświadczanie wiarygodności urządzeń dla człowieka przy użyciu jednorazowych haseł opartych na czasie
Name:		tpm2-totp
Version:	0.3.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/tpm2-software/tpm2-totp/releases
Source0:	https://github.com/tpm2-software/tpm2-totp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6665f0ae9284a3f6c56c7266f70a2a2b
URL:		https://github.com/tpm2-software/tpm2-totp
BuildRequires:	doxygen
BuildRequires:	pandoc
BuildRequires:	pkgconfig >= 1:0.25
BuildRequires:	plymouth-devel
BuildRequires:	qrencode-devel
BuildRequires:	tpm2-tss-devel >= 2
%if %{with tests}
BuildRequires:	/sbin/ss
BuildRequires:	fakeroot
BuildRequires:	iproute2-ss
BuildRequires:	oath-toolkit-devel
BuildRequires:	plymouth
# pgrep
BuildRequires:	procps
BuildRequires:	swtpm
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a reimplementation of Matthew Garrett's tpmtotp software
(<https://github.com/mjg59/tpmtotp/>) for TPM 2.0 using the tpm2-tss
software stack ((https://github.com/tpm2-software/tpm2-tss/>). Its
purpose is to attest the trustworthiness of a device against a human
using time-based one-time passwords (TOTP), facilitating the Trusted
Platform Module (TPM) to bind the TOTP secret to the known trustworthy
system state. In addition to the original tpmtotp, given the new
capabilities of in-TPM HMAC calculation, the tpm2-totp's secret HMAC
keys do not have to be exported from the TPM to the CPU's RAM on boot
anymore. Another addition is the ability to rebind an old secret to
the current PCRs in case a software component was changed on purpose,
using a user-defined password.

%description -l pl.UTF-8
Ten pakiet jest reimplementacją tpmtotp Matthew Garretta
(<https://github.com/mjg59/tpmtotp/>) dla TPM 2.0 przy użyciu stosu
tpm2-tss ((https://github.com/tpm2-software/tpm2-tss/>). Celem jest
poświadczanie wiarygodności urządzeń względem człowieka przy użyciu
jednorazowych haseł opartych na czasie (TOTP), z pomocą modułu TPM
(Trusted Platform Module) do przypisania sekretu TOTP do znanego stanu
wiarygodnego systemu. Oprócz oryginalnych możliwości tpmtotp, dzięki
nwym możliwościom obliczania HMAC w TPM, kluczy tajnych HMAC nie
trzeba już eksportować z TPM do pamięci procesora przy rozruchu
systemu. Ponadto możliwe jest przypisanie starego sekretu do obecnego
PCR w przypadku celowej zmiany oprogramowania, przy użyciu hasła
zdefiniowanego przez użytkownika.

%package devel
Summary:	Header files for tpm2-totp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tpm2-totp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for tpm2-totp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tpm2-totp.

%package static
Summary:	Static tpm2-totp library
Summary(pl.UTF-8):	Statyczna biblioteka tpm2-totp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static tpm2-totp library.

%description static -l pl.UTF-8
Statyczna biblioteka tpm2-totp.

%prep
%setup -q

%build
%configure \
	ss=/sbin/ss \
	%{?with_tests:--enable-integration} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtpm2-totp.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/tpm2-totp
%attr(755,root,root) %{_libdir}/libtpm2-totp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtpm2-totp.so.0
%dir %{_libexecdir}/tpm2-totp
%attr(755,root,root) %{_libexecdir}/tpm2-totp/plymouth-tpm2-totp
%{_mandir}/man1/tpm2-totp.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtpm2-totp.so
%{_includedir}/tpm2-totp.h
%{_pkgconfigdir}/tpm2-totp.pc
%{_mandir}/man3/tpm2-totp.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtpm2-totp.a
%endif
