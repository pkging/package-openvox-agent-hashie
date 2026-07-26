%define gem_name hashie
%define gem_cache_dir /opt/puppetlabs/puppet/share/gems

Summary:   Your friendly neighborhood hash library
Name:      openvox-agent-%{gem_name}
Version:   5.1.0
Release:   1%{?dist}
Group:     Development/Languages
License:   MIT
URL:       https://github.com/intridea/hashie
Source0:   https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires:  openvox-agent >= 8
Requires:  openvox-agent < 9
Requires:  /opt/puppetlabs/puppet/bin/gem
BuildArch: noarch
Obsoletes: puppet-agent-hashie

%description
Hashie is a collection of classes and mixins that make hashes more powerful.

%prep
%setup -q -c -T
cp -a %{SOURCE0} ./

%build

%install
mkdir -p %{buildroot}%{gem_cache_dir}
cp -a ./%{gem_name}-%{version}.gem %{buildroot}%{gem_cache_dir}

%files
%{gem_cache_dir}/%{gem_name}-%{version}.gem

%post
/opt/puppetlabs/puppet/bin/gem install --local %{gem_cache_dir}/%{gem_name}-%{version}.gem >/dev/null

%preun
if [ $1 == 0 ]; then  # uninstall
  /opt/puppetlabs/puppet/bin/gem uninstall -x -v %{version} %{gem_name} >/dev/null
else  # upgrade
  # Only uninstall on upgrade if there are multiple gem versions installed, as the package
  # is probably changing version, not only undergoing a release bump
  if ! /opt/puppetlabs/puppet/bin/gem list %{gem_name} | grep %{gem_name} | grep -q '(%{version})'; then
    /opt/puppetlabs/puppet/bin/gem uninstall -x -v %{version} %{gem_name} >/dev/null
  fi
fi

%changelog
* Sun Jul 26 2026 Lennart Betz <lbetz@prefork.de> - 5.1.0-1
- Release v5.1.0, rename package, remove OpenVox 7 support
* Fri Aug 30 2024 Lennart Betz <lennart.betz@netways.de> - 5.0.0-1
- Release v5.0.0
