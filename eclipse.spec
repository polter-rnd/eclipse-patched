# Set to build Eclipse without circular dependency to eclipse-pde, API
# generation and docs will not be built and a second run will be required, but
# this is a way to bootstrap Eclipse on secondary archs.
%bcond_with bootstrap

Epoch:                  1

%global eb_commit       e3e8e3f486014f5683f9200a981f313800b8c964
%global eclipse_rel     %{version}
%global eclipse_tag     R-%{eclipse_rel}-202009021800

%global _jetty_version  9.4.33
%global _lucene_version 8.6.3
%global _batik_version 1.13
%global _asm_version 8.0.1

%global _emf_version 1:2.23.0
%global _ecf_version 3.14.17

%ifarch s390x x86_64 aarch64 ppc64le
    %global eclipse_arch %{_arch}
%endif

# Desktop file information
%global app_name %{?app_name_prefix}%{!?app_name_prefix:Eclipse}
%global app_exec %{?app_exec_prefix} eclipse

# Eclipse is arch-specific, but multilib agnostic
%global _eclipsedir %{_prefix}/lib/eclipse

%if 0%{?fedora} || 0%{?rhel} > 7 || 0%{?eln}
%global use_wayland 1
%else
%global use_wayland 0
%endif

# Glassfish EE APIs that moved to jakarta namespace
%if 0%{?fedora} >= 33 || 0%{?eln}
%global _jakarta_annotations jakarta.annotation-api
%global _jakarta_servlet_api jakarta.servlet-api
%global _jakarta_jsp_api javax.servlet.jsp-api
%global _jakarta_jsp org.glassfish.web.jakarta.servlet.jsp
%global _jakarta_el_api jakarta.el-api
%global _jakarta_el org.glassfish.jakarta.el
%else
%global _jakarta_annotations javax.annotation-api
%global _jakarta_servlet_api javax.servlet-api
%global _jakarta_jsp_api javax.servlet.jsp
%global _jakarta_jsp org.glassfish.web.javax.servlet.jsp
%global _jakarta_el_api javax.el-api
%global _jakarta_el com.sun.el.javax.el
%endif

Summary:        An open, extensible IDE
Name:           eclipse
Version:        4.17
Release:        4.patched%{?dist}
License:        EPL-2.0
URL:            https://www.eclipse.org/

Source0: https://download.eclipse.org/eclipse/downloads/drops4/%{eclipse_tag}/eclipse-platform-sources-%{eclipse_rel}.tar.xz

# Can generate locally with:
# git archive --format=tar --prefix=org.eclipse.linuxtools.eclipse-build-%%{eb_commit}/ \
#   %%{eb_commit} | xz > org.eclipse.linuxtools.eclipse-build-%%{eb_commit}.tar.xz
Source1: https://git.eclipse.org/c/linuxtools/org.eclipse.linuxtools.eclipse-build.git/snapshot/org.eclipse.linuxtools.eclipse-build-%{eb_commit}.tar.xz

# Eclipse should not include source for dependencies that are not supplied by this package
# and should not include source for bundles that are not relevant to our platform
Patch0:  eclipse-no-source-for-dependencies.patch

# https://bugs.eclipse.org/bugs/show_bug.cgi?id=377515
Patch1:  eclipse-p2-pick-up-renamed-jars.patch

# Patch for this was contributed. Unlikely to be released.
Patch2:  eclipse-ignore-version-when-calculating-home.patch

# Explicit requirement on hamcrest where it is used directly
Patch3:  explicit-hamcrest.patch

# Add support for all arches supported by Fedora
Patch4:  eclipse-secondary-arches.patch

Patch5:  eclipse-debug-symbols.patch

# https://bugs.eclipse.org/bugs/show_bug.cgi?id=408138
Patch12: eclipse-fix-dropins.patch

# Feature plugin definitions lock onto version of plugin at build-time.
# If plugin is external, updating it breaks the feature. (version changes)
# Workaround : Change <plugin> definition to a 'requirement'
Patch13: eclipse-feature-plugins-to-category-ius.patch

Patch14: eclipse-support-symlink-bundles.patch

# Fix various JDT and PDE tests
Patch15: eclipse-fix-tests.patch

# Droplet fixes
Patch17: eclipse-pde-tp-support-droplets.patch

# Disable uses by default
Patch18: eclipse-disable-uses-constraints.patch

# Droplet fixes
Patch19: eclipse-make-droplets-runnable.patch
Patch20: eclipse-disable-droplets-in-dropins.patch

# Temporary measure until wayland improves
Patch21: prefer_x11_backend.patch

# Fix errors when building ant launcher
Patch22: fix_ant_build.patch

# Hide the p2 Droplets from cluttering Install Wizard Combo
Patch23: eclipse-hide-droplets-from-install-wizard.patch

# Avoid the need for a javascript interpreter at build time
Patch24: eclipse-swt-avoid-javascript-at-build.patch

# Avoid optional dep used only for tests
Patch25: eclipse-patch-out-fileupload-dep.patch

# Force a clean on the restart after p2 operations
Patch26: force-clean-after-p2-operations.patch

# Disable message box asking to restart if zoom has been changed
Patch27: disable_zoom_changed_message.patch

# Upstream no longer supports non-64bit arches
ExcludeArch: s390 %{arm} %{ix86}

BuildRequires: java-11-openjdk-devel

BuildRequires: maven-local
BuildRequires: tycho
BuildRequires: tycho-extras
BuildRequires: cbi-plugins
BuildRequires: maven-antrun-plugin
BuildRequires: maven-assembly-plugin
BuildRequires: maven-dependency-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-shade-plugin
BuildRequires: xml-maven-plugin
BuildRequires: rsync
BuildRequires: make, gcc
BuildRequires: zip, unzip
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(nspr)
BuildRequires: pkgconfig(glu)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(webkit2gtk-4.0)
BuildRequires: icu4j >= 1:65.1
BuildRequires: ant >= 1.10.9
BuildRequires: ant-antlr ant-apache-bcel ant-apache-oro ant-apache-regexp ant-apache-resolver ant-commons-logging ant-apache-bsf
BuildRequires: ant-commons-net ant-javamail ant-jdepend ant-junit ant-swing ant-jsch ant-testutil ant-apache-xalan2 ant-jmf ant-xz ant-junit5
BuildRequires: jsch
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-codec
BuildRequires: apache-commons-jxpath
BuildRequires: osgi(org.apache.felix.gogo.shell) >= 1.1.0
BuildRequires: osgi(org.apache.felix.gogo.command) >= 1.0.2
BuildRequires: osgi(org.apache.felix.gogo.runtime) >= 1.1.0
BuildRequires: felix-scr >= 2.1.16-4
BuildRequires: osgi(org.eclipse.jetty.util) >= %{_jetty_version}
BuildRequires: osgi(org.eclipse.jetty.server) >= %{_jetty_version}
BuildRequires: osgi(org.eclipse.jetty.http) >= %{_jetty_version}
BuildRequires: osgi(org.eclipse.jetty.continuation) >= %{_jetty_version}
BuildRequires: osgi(org.eclipse.jetty.io) >= %{_jetty_version}
BuildRequires: osgi(org.eclipse.jetty.security) >= %{_jetty_version}
BuildRequires: osgi(org.eclipse.jetty.servlet) >= %{_jetty_version}
BuildRequires: lucene-core >= %{_lucene_version}
BuildRequires: lucene-analysis >= %{_lucene_version}
BuildRequires: lucene-queryparser >= %{_lucene_version}
BuildRequires: lucene-analyzers-smartcn >= %{_lucene_version}
BuildRequires: junit >= 4.12
BuildRequires: junit5 >= 5.4.0
BuildRequires: apiguardian
BuildRequires: hamcrest
BuildRequires: sat4j
BuildRequires: objectweb-asm >= %{_asm_version}
BuildRequires: sac
BuildRequires: batik-css >= %{_batik_version}
BuildRequires: batik-util >= %{_batik_version}
BuildRequires: google-gson
BuildRequires: xmlgraphics-commons >= 2.3
BuildRequires: xml-commons-apis
BuildRequires: atinject
BuildRequires: eclipse-ecf-core >= %{_ecf_version}
BuildRequires: eclipse-emf-core >= %{_emf_version}
BuildRequires: eclipse-license2
BuildRequires: glassfish-annotation-api
BuildRequires: glassfish-el-api >= 3.0.1
BuildRequires: glassfish-el >= 3.0.1
BuildRequires: glassfish-jsp-api >= 2.2.1-4
BuildRequires: glassfish-jsp >= 2.2.5
BuildRequires: glassfish-servlet-api >= 3.1.0
BuildRequires: httpcomponents-core
BuildRequires: httpcomponents-client
BuildRequires: jsoup
BuildRequires: xz-java
BuildRequires: osgi(osgi.annotation)
BuildRequires: jna
BuildRequires: jna-contrib
# Build deps that are excluded when bootstrapping
%if %{without bootstrap}
# For building docs and apitooling
BuildRequires: eclipse-pde
%endif

%description
The Eclipse platform is designed for building integrated development
environments (IDEs), server-side applications, desktop applications, and
everything in between.

%package        swt
Summary:        SWT Library for GTK+
Requires:       gtk3
Requires:       webkitgtk4

%description swt
SWT Library for GTK+.

%package        equinox-osgi
Summary:        Eclipse OSGi - Equinox
Provides:       osgi(system.bundle) = %{epoch}:%{version}

%description  equinox-osgi
Eclipse OSGi - Equinox

%package        platform
Summary:        Eclipse platform common files
Requires:       java-11-openjdk-devel
Requires:       javapackages-tools
Obsoletes:      eclipse-usage < 4.17.0-1

Requires: ant >= 1.10.9
Requires: ant-antlr ant-apache-bcel ant-apache-oro ant-apache-regexp ant-apache-resolver ant-commons-logging ant-apache-bsf
Requires: ant-commons-net ant-javamail ant-jdepend ant-junit ant-swing ant-jsch ant-testutil ant-apache-xalan2 ant-jmf ant-xz ant-junit5
Requires: apache-commons-logging
Requires: apache-commons-codec
Requires: apache-commons-jxpath
Requires: osgi(org.apache.felix.gogo.shell) >= 1.1.0
Requires: osgi(org.apache.felix.gogo.command) >= 1.0.2
Requires: osgi(org.apache.felix.gogo.runtime) >= 1.1.0
Requires: felix-scr >= 2.1.16-4
Requires: osgi(org.eclipse.jetty.util) >= %{_jetty_version}
Requires: osgi(org.eclipse.jetty.server) >= %{_jetty_version}
Requires: osgi(org.eclipse.jetty.http) >= %{_jetty_version}
Requires: osgi(org.eclipse.jetty.continuation) >= %{_jetty_version}
Requires: osgi(org.eclipse.jetty.io) >= %{_jetty_version}
Requires: osgi(org.eclipse.jetty.security) >= %{_jetty_version}
Requires: osgi(org.eclipse.jetty.servlet) >= %{_jetty_version}
Requires: lucene-core >= %{_lucene_version}
Requires: lucene-analysis >= %{_lucene_version}
Requires: lucene-queryparser >= %{_lucene_version}
Requires: lucene-analyzers-smartcn >= %{_lucene_version}
Requires: batik-css >= %{_batik_version}
Requires: batik-util >= %{_batik_version}
Requires: xmlgraphics-commons >= 2.3
Requires: xml-commons-apis
Requires: atinject
Requires: eclipse-ecf-core >= %{_ecf_version}
Requires: eclipse-emf-core >= %{_emf_version}
Requires: glassfish-annotation-api
Requires: glassfish-el-api >= 3.0.1
Requires: glassfish-el >= 3.0.1
Requires: glassfish-jsp-api >= 2.2.1-4
Requires: glassfish-jsp >= 2.2.5
Requires: glassfish-servlet-api >= 3.1.0
Requires: icu4j >= 1:65.1
Requires: %{name}-swt = %{epoch}:%{version}-%{release}
Requires: %{name}-equinox-osgi = %{epoch}:%{version}-%{release}
Requires: httpcomponents-core
Requires: httpcomponents-client

# Obsoletes added in F31
Obsoletes: eclipse-epp-logging <= 2.0.8-4
Obsoletes: eclipse-abrt <= 0.0.3-10

# No longer shipping tests and contrib tools since F33
Obsoletes:      %{name}-tests < 1:4.17-4
Obsoletes:      %{name}-contributor-tools < 1:4.17-4

%description    platform
The Eclipse Platform is the base of all IDE plugins.  This does not include the
Java Development Tools or the Plugin Development Environment.

%package        jdt
Summary:        Eclipse Java Development Tools
BuildArch:      noarch

Provides:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{name}-platform = %{epoch}:%{version}-%{release}
Requires:       junit >= 4.12
Requires:       junit5 >= 5.4.0
Requires:       osgi(org.hamcrest.core)

# Obsoletes added in F30
Obsoletes: eclipse-recommenders <= 2.5.4-5

%description    jdt
Eclipse Java Development Tools.  This package is required to use Eclipse for
developing software written in the Java programming language.

%package        pde
Summary:        Eclipse Plugin Development Environment

Requires:       %{name}-platform = %{epoch}:%{version}-%{release}
Requires:       %{name}-jdt = %{epoch}:%{version}-%{release}
Requires:       objectweb-asm >= %{_asm_version}

%description    pde
Eclipse Plugin Development Environment.  This package is required for
developing Eclipse plugins.

%package        p2-discovery
Summary:        Eclipse p2 Discovery
BuildArch:      noarch

Requires:       %{name}-platform = %{epoch}:%{version}-%{release}

%description    p2-discovery
The p2 Discovery mechanism provides a simplified and branded front-end for the
p2 provisioning platform. Discovery can be used as a tool to display and
install from existing P2 repositories or as a framework to build branded
installer UIs.

%prep
%setup -T -c

# Extract main source
tar --strip-components=1 -xf %{SOURCE0}

# Extract linuxtools/eclipse-build sources
tar --strip-components=1 -xf %{SOURCE1}

# Delete pre-built binary artifacts except some test data that cannot be generated
find . ! -path "*/JCL/*" ! -name "rtstubs*.jar" ! -name "java14api.jar" ! -name "j9stubs.jar" ! -name "annotations.jar" \
   -type f -name *.jar -delete
find . -type f -name *.class -delete
find . -type f -name *.so -delete
find . -type f -name *.dll -delete
find . -type f -name *.jnilib -delete

# Remove pre-compiled native launchers
rm -rf rt.equinox.binaries/org.eclipse.equinox.executable/{bin,contributed}/

%patch0
%patch1
%patch2 -p1
%patch3
%patch4 -p1
%patch5
%patch12
%patch13 -p1
%patch14
%patch15
%patch17 -p1
%patch18
%patch19
%patch20
%if ! %{use_wayland}
# Enable wayland by default on F27+
%patch21
%endif
%patch22
%patch23 -p1
%patch24 -p1
%patch25
%patch26 -p1
%patch27

# Optional (unused) multipart support (see patch 25)
rm rt.equinox.bundles/bundles/org.eclipse.equinox.http.servlet/src/org/eclipse/equinox/http/servlet/internal/multipart/MultipartSupport{Impl,FactoryImpl,Part}.java

# Remove jgit deps because building from source tarball, not a git repo
%pom_remove_dep :tycho-buildtimestamp-jgit eclipse-platform-parent
%pom_remove_dep :tycho-sourceref-jgit eclipse-platform-parent
%pom_xpath_remove 'pom:configuration/pom:timestampProvider' eclipse-platform-parent
%pom_xpath_remove 'pom:configuration/pom:sourceReferences' eclipse-platform-parent

# Resolving the target platform requires too many changes, so don't use it
%pom_xpath_remove "pom:configuration/pom:target" eclipse-platform-parent

# Disable as many products as possible to make the build faster, we care only for the IDE
%pom_disable_module platform.sdk eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module rcp eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module rcp.sdk eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module rcp.config eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module sdk eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module equinox-sdk eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module equinox.starterkit.product eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module eclipse.platform.repository eclipse.platform.releng.tychoeclipsebuilder

# Disable bundles that we don't ship as part of the remaining products
%pom_disable_module bundles/org.eclipse.equinox.cm.test rt.equinox.bundles
%pom_disable_module features/org.eclipse.equinox.sdk rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.console.jaas.fragment rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.console.ssh rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.transforms.xslt rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.transforms.hook rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.weaving.caching.j9 rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.weaving.caching rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.weaving.hook rt.equinox.bundles
%pom_disable_module features/org.eclipse.equinox.compendium.sdk rt.equinox.bundles
%pom_disable_module features/org.eclipse.equinox.core.sdk rt.equinox.bundles
%pom_disable_module features/org.eclipse.equinox.p2.sdk rt.equinox.p2
%pom_disable_module features/org.eclipse.equinox.server.p2 rt.equinox.bundles
%pom_disable_module features/org.eclipse.equinox.serverside.sdk rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.p2.artifact.checksums.bouncycastle rt.equinox.p2

# Don't need annotations for obsolete JDKs
%pom_disable_module org.eclipse.jdt.annotation_v1 eclipse.jdt.core
%pom_xpath_remove "plugin[@version='1.1.500.qualifier']" eclipse.jdt/org.eclipse.jdt-feature/feature.xml

# javax.annotation -> jakarta.annotation-api
# javax.servlet -> jakarta.servlet-api
# javax.el -> jakarta.el-api
# javax.servlet.jsp -> jakarta.servlet.jsp-api
sed -i -e 's/javax.annotation/%{_jakarta_annotations}/' -e 's/javax.servlet\([^.]\)/%{_jakarta_servlet_api}\1/' \
       -e 's/javax.el/%{_jakarta_el_api}/' -e 's/com.sun.el/%{_jakarta_el}/' \
       -e 's/javax.servlet.jsp/%{_jakarta_jsp_api}/' -e 's/org.apache.jasper.glassfish/%{_jakarta_jsp}/' \
  eclipse-platform-parent/pom.xml \
  eclipse.platform.releng/features/org.eclipse.help-feature/feature.xml \
  eclipse.platform.common/bundles/org.eclipse.*/pom.xml \
  eclipse.platform.common/bundles/org.eclipse.platform.doc.isv/platformOptions.txt \
  eclipse.platform.ui/features/org.eclipse.e4.rcp/feature.xml \
  rt.equinox.bundles/features/org.eclipse.equinox.server.{jetty,simple}/feature.xml

# Fix requirement on junit 4
sed -i -e 's/4.13.0,5.0.0/4.12.0,5.0.0/' eclipse.jdt.ui/org.eclipse.jdt.junit.core/src/org/eclipse/jdt/internal/junit/buildpath/BuildPathSupport.java

# Disable examples
%pom_disable_module infocenter-web eclipse.platform.ua
%pom_disable_module examples rt.equinox.p2
%pom_disable_module examples eclipse.platform.ui
%pom_disable_module org.eclipse.debug.examples.core eclipse.platform.debug
%pom_disable_module org.eclipse.debug.examples.memory eclipse.platform.debug
%pom_disable_module org.eclipse.debug.examples.mixedmode eclipse.platform.debug
%pom_disable_module org.eclipse.debug.examples.ui eclipse.platform.debug
%pom_disable_module bundles/org.eclipse.sdk.examples eclipse.platform.releng
%pom_disable_module features/org.eclipse.sdk.examples-feature eclipse.platform.releng
%pom_disable_module examples/org.eclipse.swt.examples.ole.win32 eclipse.platform.swt
%pom_disable_module examples/org.eclipse.compare.examples eclipse.platform.team
%pom_disable_module examples/org.eclipse.compare.examples.xml eclipse.platform.team
%pom_disable_module examples/org.eclipse.team.examples.filesystem eclipse.platform.team
%pom_disable_module org.eclipse.jface.text.examples eclipse.platform.text
%pom_disable_module org.eclipse.ui.examples.javaeditor eclipse.platform.text
%pom_disable_module org.eclipse.ui.genericeditor.examples eclipse.platform.text
%pom_disable_module org.eclipse.ui.intro.quicklinks.examples eclipse.platform.ua
%pom_disable_module org.eclipse.ui.intro.solstice.examples eclipse.platform.ua

# Disable tests
for pom in eclipse.jdt.core{,.binaries} eclipse.jdt.debug eclipse.jdt.ui eclipse.pde.build eclipse.pde.ui{,/apitools} \
    eclipse.platform eclipse.platform.debug eclipse.platform.releng eclipse.platform.resources eclipse.platform.runtime \
    eclipse.platform.swt eclipse.platform.team eclipse.platform.text eclipse.platform.ui eclipse.platform.ua \
    rt.equinox.bundles rt.equinox.framework rt.equinox.p2 ; do
  sed -i -e '/<module>.*tests.*<\/module>/d' $pom/pom.xml
done
%pom_disable_module bundles/org.eclipse.equinox.frameworkadmin.test rt.equinox.p2
%pom_disable_module eclipse-junit-tests eclipse.platform.releng.tychoeclipsebuilder
%pom_disable_module ./tests/org.eclipse.e4.tools.test eclipse.platform.ui.tools

# Disable test framework if we are not shipping tests
%pom_disable_module features/org.eclipse.test-feature eclipse.platform.releng
%pom_disable_module bundles/org.eclipse.test eclipse.platform.releng
%pom_disable_module bundles/org.eclipse.test.performance eclipse.platform.releng
%pom_disable_module bundles/org.eclipse.test.performance.win32 eclipse.platform.releng
%pom_disable_module bundles/org.eclipse.ant.optional.junit eclipse.platform.releng

# Disable servletbridge stuff
%pom_disable_module bundles/org.eclipse.equinox.http.servletbridge rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.servletbridge rt.equinox.bundles
%pom_disable_module bundles/org.eclipse.equinox.servletbridge.template rt.equinox.bundles

# Don't need enforcer on RPM builds
%pom_remove_plugin :maven-enforcer-plugin eclipse-platform-parent

# This part generates secondary fragments using primary fragments
rm -rf eclipse.platform.swt.binaries/bundles/org.eclipse.swt.gtk.linux.s390x
rm -rf rt.equinox.framework/bundles/org.eclipse.equinox.launcher.gtk.linux.s390x
for dir in rt.equinox.binaries rt.equinox.framework/bundles eclipse.platform.swt.binaries/bundles ; do
  utils/ensure_arch.sh "$dir" x86_64 s390x
done

# Remove platform-specific stuff that we don't care about to reduce build time
# (i.e., all bundles that are not applicable to the current build platform --
# this reduces the build time on arm by around 20 minutes per architecture that
# we are not currently building)
TYCHO_ENV="<environment><os>linux</os><ws>gtk</ws><arch>%{eclipse_arch}</arch></environment>"
%pom_xpath_set "pom:configuration/pom:environments" "$TYCHO_ENV" eclipse-platform-parent
%pom_xpath_set "pom:configuration/pom:environments" "$TYCHO_ENV" eclipse.platform.ui/bundles/org.eclipse.e4.ui.swt.gtk
for b in `ls eclipse.platform.swt.binaries/bundles | grep -P -e 'org.eclipse.swt\.(?!gtk\.linux.%{eclipse_arch}$)'` ; do
  module=$(grep ">bundles/$b<" eclipse.platform.swt.binaries/pom.xml || :)
  if [ -n "$module" ] ; then
    %pom_disable_module bundles/$b eclipse.platform.swt.binaries
    %pom_xpath_inject "pom:excludes" "<plugin id='$b'/>" eclipse.platform.ui/features/org.eclipse.e4.rcp
  fi
done
for b in `ls rt.equinox.framework/bundles | grep -P -e 'org.eclipse.equinox.launcher\.(?!gtk\.linux.%{eclipse_arch}$)'` ; do
  module=$(grep ">bundles/$b<" rt.equinox.framework/pom.xml || :)
  if [ -n "$module" ] ; then
    %pom_disable_module bundles/$b rt.equinox.framework
    %pom_xpath_remove -f "plugin[@id='$b']" rt.equinox.framework/features/org.eclipse.equinox.executable.feature/feature.xml
  fi
done
for b in `(cd rt.equinox.bundles/bundles && ls -d *{macosx,win32,linux}*) | grep -P -e 'org.eclipse.equinox.security\.(?!linux\.%{eclipse_arch}$)'` ; do
  module=$(grep ">bundles/$b<" rt.equinox.bundles/pom.xml || :)
  if [ -n "$module" ] ; then
    %pom_disable_module bundles/$b rt.equinox.bundles
    %pom_xpath_remove -f "plugin[@id='$b']" rt.equinox.p2/features/org.eclipse.equinox.p2.core.feature/feature.xml
  fi
done
for b in `ls eclipse.platform.team/bundles/ | grep -P -e 'org.eclipse.core.net\.(?!linux.%{eclipse_arch}$)'` ; do
  %pom_disable_module bundles/$b eclipse.platform.team
done
for b in `ls eclipse.platform.resources/bundles/ | grep -P -e 'org.eclipse.core.filesystem\.(?!linux\.%{eclipse_arch}$)'` ; do
  module=$(grep ">bundles/$b<" eclipse.platform.resources/pom.xml || :)
  if [ -n "$module" ] ; then
    %pom_disable_module bundles/$b eclipse.platform.resources
  fi
done
%pom_disable_module org.eclipse.jdt.launching.macosx eclipse.jdt.debug
%pom_disable_module org.eclipse.jdt.launching.ui.macosx eclipse.jdt.debug
%pom_disable_module bundles/org.eclipse.compare.win32 eclipse.platform.team
%pom_disable_module org.eclipse.e4.ui.workbench.renderers.swt.cocoa eclipse.platform.ui/bundles
%pom_disable_module org.eclipse.ui.cocoa eclipse.platform.ui/bundles
%pom_disable_module org.eclipse.ui.win32 eclipse.platform.ui/bundles
%pom_disable_module org.eclipse.e4.ui.swt.win32 eclipse.platform.ui/bundles
%pom_disable_module bundles/org.eclipse.core.resources.win32.x86_64 eclipse.platform.resources
%pom_disable_module bundles/org.eclipse.swt.browser.chromium eclipse.platform.swt
%pom_xpath_remove -f "plugin[@id='org.eclipse.swt.browser.chromium.gtk.linux.x86_64']" eclipse.platform.ui/features/org.eclipse.e4.rcp/feature.xml
for f in eclipse.jdt/org.eclipse.jdt-feature/feature.xml \
         eclipse.platform.ui/features/org.eclipse.e4.rcp/feature.xml \
         eclipse.platform.releng/features/org.eclipse.rcp/feature.xml \
         eclipse.platform.releng/features/org.eclipse.platform-feature/feature.xml ; do
  %pom_xpath_remove -f "plugin[@os='macosx']" $f
  %pom_xpath_remove -f "plugin[@os='win32']" $f
  %pom_xpath_remove -f "plugin[@ws='win32']" $f
  for arch in x86_64 aarch64 ppc64le s390x ; do
    if [ "$arch" != "%{eclipse_arch}" ] ; then
      %pom_xpath_remove -f "plugin[@arch='$arch']" $f
    fi
  done
done

# Fix javadoc generation relying on Windows version of SWT
sed -i -e '/swt/s/swt.win32.win32.x86_64/swt.gtk.linux.%{eclipse_arch}/' eclipse.platform.common/bundles/org.eclipse*/*Options.txt

# Disable contributor tools
%pom_disable_module eclipse.platform.ui.tools
%pom_disable_module features/org.eclipse.swt.tools.feature eclipse.platform.swt
%pom_disable_module bundles/org.eclipse.swt.tools.base eclipse.platform.swt
%pom_disable_module bundles/org.eclipse.swt.tools.spies eclipse.platform.swt
%pom_disable_module bundles/org.eclipse.swt.tools eclipse.platform.swt
%pom_disable_module features/org.eclipse.releng.tools eclipse.platform.releng
%pom_disable_module bundles/org.eclipse.releng.tools eclipse.platform.releng

# Include some extra features with the product that some other projects may need at
# build time as part of their target platform definitions
sed -i -e '/<features>/a<feature id="org.eclipse.core.runtime.feature"/>' \
  eclipse.platform.releng.tychoeclipsebuilder/platform/platform.product

# Ensure batch compiler gets installed correctly
%pom_xpath_inject 'feature' '<plugin id="org.eclipse.jdt.core.compiler.batch" download-size="0" install-size="0" version="0.0.0" unpack="false"/>' \
  eclipse.platform.releng/features/org.eclipse.platform-feature/feature.xml
sed -i -e '/<\/excludes>/i<plugin id="org.eclipse.jdt.core.compiler.batch"/>' \
  eclipse.platform.releng/features/org.eclipse.platform-feature/pom.xml

# Don't set perms on files for platforms that aren't linux
for f in rt.equinox.framework/features/org.eclipse.equinox.executable.feature/build.properties; do
  grep '^root\.linux\.gtk\.%{eclipse_arch}[.=]' $f > tmp
  sed -i -e '/^root\./d' $f && cat tmp >> $f
done

# Hack - this can go away once upstream grows arm and aarch64 support
mkdir -p rt.equinox.binaries/org.eclipse.equinox.executable/bin/gtk/linux/%{eclipse_arch}

# Ensure that bundles with native artifacts are dir-shaped, so no *.so is extracted into user.home
for f in eclipse.platform.swt.binaries/bundles/org.eclipse.swt.gtk.linux.*/META-INF/MANIFEST.MF \
         eclipse.platform.resources/bundles/org.eclipse.core.filesystem.linux.*/META-INF/MANIFEST.MF \
         eclipse.platform.team/bundles/org.eclipse.core.net.linux.*/META-INF/MANIFEST.MF ; do
    echo -e "Eclipse-BundleShape: dir\n\n" >> $f;
done

# Build fake ant bundle that contains symlinks to system jars
dependencies/fake_ant_dependency.sh

# Allow usage of javax.servlet.jsp 2.3.
sed -i '/javax\.servlet\.jsp/ s/2\.3/2\.4/' rt.equinox.bundles/bundles/org.eclipse.equinox.jsp.jasper/META-INF/MANIFEST.MF

# Fix constraint on gogo runtime
sed -i -e '/org.apache.felix.service.command/s/;status=provisional//' rt.equinox.bundles/bundles/org.eclipse.equinox.console{,.ssh}/META-INF/MANIFEST.MF

# Pre-compiling JSPs does not currently work
%pom_remove_plugin org.eclipse.jetty:jetty-jspc-maven-plugin eclipse.platform.ua/org.eclipse.help.webapp

# Make maven output less noisy due to lack of intenet connection
sed -i -e '/baselineMode/s/warn/disable/' eclipse-platform-parent/pom.xml

# Use system osgi.annotation lib
ln -s $(build-classpath osgi-annotation) rt.equinox.framework/bundles/org.eclipse.osgi/osgi/
ln -s $(build-classpath osgi-annotation) rt.equinox.framework/bundles/org.eclipse.osgi.services/lib/
ln -s $(build-classpath osgi-annotation) rt.equinox.framework/bundles/org.eclipse.osgi.util/lib/
ln -s $(build-classpath osgi-annotation) rt.equinox.bundles/bundles/org.eclipse.equinox.http.servlet/osgi/
ln -s $(build-classpath osgi-annotation) rt.equinox.bundles/bundles/org.eclipse.equinox.coordinator/lib/
ln -s $(build-classpath osgi-annotation) rt.equinox.bundles/bundles/org.eclipse.equinox.log.stream/osgi/

# The order of these mvn_package calls is important
%mvn_package "::pom::" __noinstall
%mvn_package "::jar:sources{,-feature}:" sdk
%mvn_package ":org.eclipse.jdt.doc.isv" sdk
%mvn_package ":org.eclipse.platform.doc.isv" sdk
%mvn_package ":org.eclipse.equinox.executable" sdk
%mvn_package "org.eclipse.jdt{,.feature}:" jdt
%mvn_package ":org.eclipse.ant.{launching,ui}" jdt
%mvn_package ":org.eclipse.equinox.p2.discovery.{feature,compatibility}" p2-discovery
%mvn_package ":org.eclipse.equinox.p2{,.ui}.discovery" p2-discovery
%mvn_package "org.eclipse.cvs{,.feature}:" cvs
%mvn_package "org.eclipse.team:org.eclipse.team.cvs*" cvs
%mvn_package "org.eclipse.pde{,.ui,.feature}:" pde
%mvn_package ":org.eclipse.pde.api.tools*" pde
%mvn_package "org.eclipse.ui:org.eclipse.ui.trace" pde
%mvn_package "org.eclipse.sdk{,.feature}:" sdk
%mvn_package ":" __noinstall

%build
# Compiler/linker flags for native parts
export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
export M_CFLAGS="$CFLAGS"
export M_ARCH="$LDFLAGS"

#This is the lowest value where the build succeeds. 512m is not enough.
export MAVEN_OPTS="-Dfile.encoding=UTF-8 -Xmx1024m -XX:CompileCommand=exclude,org/eclipse/tycho/core/osgitools/EquinoxResolver,newState ${MAVEN_OPTS}"

# TODO: Fix bug in the tycho installation
xmvn -o install:install-file -Dtycho.mode=maven -Dfile=%{_javadir}/tycho/tycho-lib-detector.jar -DpomFile=%{_mavenpomdir}/tycho/tycho-lib-detector.pom

# Pre-build agent jar needed for AdvancedSourceLookupSupport
(cd eclipse.jdt.debug/org.eclipse.jdt.launching.javaagent && xmvn -e -o -B clean verify)
mv eclipse.jdt.debug/org.eclipse.jdt.launching.javaagent/target/javaagent-shaded.jar \
  eclipse.jdt.debug/org.eclipse.jdt.launching/lib

# Qualifier generated from last modification time of source tarball
QUALIFIER=$(date -u -d"$(stat --format=%y %{SOURCE0})" +v%Y%m%d-%H%M)
%mvn_build -j -f -- -e -DforceContextQualifier=$QUALIFIER -DaggregatorBuild=true \
%if %{with bootstrap}
   api-generation,!build-docs \
%endif
   -Declipse.javadoc=%{_jvmdir}/java-11/bin/javadoc -Dnative=gtk.linux.%{eclipse_arch} \
   -Dtycho.local.keepTarget -DskipRust=true -DskipJni=true \
   -Dfedora.p2.repos=$(pwd)/.m2/p2/repo-sdk/plugins -DbuildType=X

# Location that the product is materialised
product="eclipse.platform.releng.tychoeclipsebuilder/platform/target/products/org.eclipse.platform.ide/linux/gtk/%{eclipse_arch}"

# Re-symlink ant bundle to use system jars
dependencies/fake_ant_dependency.sh $product/eclipse/plugins/org.apache.ant_*

# Symlink necessary plugins that are provided by other packages
dependencies/replace_platform_plugins_with_symlinks.sh $product/eclipse %{_javadir} %{_jnidir}

pushd $product/eclipse

#clean up
rm -rf configuration/org.eclipse.core.runtime
rm -rf configuration/org.eclipse.equinox.app
rm -rf configuration/org.eclipse.update
rm -rf configuration/org.eclipse.osgi
rm -rf p2/org.eclipse.equinox.p2.core/cache/*
# no icon needed
rm -f icon.xpm

# EMF and ECF are packaged separately
rm -rf features/org.eclipse.emf.* plugins/org.eclipse.emf.* \
  features/org.eclipse.ecf.* plugins/org.eclipse.ecf.* plugins/org.eclipse.ecf_*

#delete all local repositories. We want to have only "original" by default.
pushd p2/org.eclipse.equinox.p2.engine/.settings
    sed -i "/repositories\/file/d" *.prefs ../profileRegistry/SDKProfile.profile/.data/.settings/*.prefs
    sed -i "/repositories\/memory/d" *.prefs ../profileRegistry/SDKProfile.profile/.data/.settings/*.prefs
popd

# ini file adjustements
sed -i "s|-Xms40m|-Xms512m|g" eclipse.ini
sed -i "s|-Xmx512m|-Xmx1024m|g" eclipse.ini
sed -i '1i-protect\nroot' eclipse.ini
sed -i '/-vmargs/i-vm\n%{_jvmdir}/java-11/bin/java' eclipse.ini

# Temporary fix until https://bugs.eclipse.org/294877 is resolved
cat >> eclipse.ini <<EOF
-Dorg.eclipse.swt.browser.UseWebKitGTK=true
-Dorg.eclipse.equinox.p2.reconciler.dropins.directory=%{_datadir}/eclipse/dropins
-Dp2.fragments=%{_eclipsedir}/droplets,%{_datadir}/eclipse/droplets
-Declipse.p2.skipMovedInstallDetection=true
-Dosgi.resolver.usesMode=ignore
EOF

popd #eclipse

%install
%mvn_install

# Some directories we need
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}
install -d -m 755 $RPM_BUILD_ROOT%{_jnidir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/eclipse
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}

# Install icons
install -D eclipse.platform/platform/org.eclipse.platform/eclipse32.png \
    $RPM_BUILD_ROOT/usr/share/icons/hicolor/32x32/apps/%{name}.png
install -D eclipse.platform/platform/org.eclipse.platform/eclipse48.png \
    $RPM_BUILD_ROOT/usr/share/icons/hicolor/48x48/apps/%{name}.png
install -D eclipse.platform/platform/org.eclipse.platform/eclipse256.png \
    $RPM_BUILD_ROOT/usr/share/icons/hicolor/256x256/apps/%{name}.png
install -d $RPM_BUILD_ROOT/usr/share/pixmaps
ln -s /usr/share/icons/hicolor/256x256/apps/%{name}.png \
    $RPM_BUILD_ROOT/usr/share/pixmaps/%{name}.png

# Install desktop file
sed -i -e 's/Exec=eclipse/Exec=%{app_exec}/g' desktopintegration/eclipse.desktop
sed -i -e 's/Name=Eclipse/Name=%{app_name}/g' desktopintegration/eclipse.desktop
sed -i -e 's/Icon=eclipse/Icon=%{name}/g' desktopintegration/eclipse.desktop
install -m644 -D desktopintegration/eclipse.desktop $RPM_BUILD_ROOT/usr/share/applications/%{name}.desktop
desktop-file-validate $RPM_BUILD_ROOT/usr/share/applications/%{name}.desktop

# Install appstream appdata
install -m644 -D desktopintegration/eclipse.appdata.xml      $RPM_BUILD_ROOT%{_datadir}/appdata/eclipse.appdata.xml
install -m644 -D desktopintegration/eclipse-jdt.metainfo.xml $RPM_BUILD_ROOT%{_datadir}/appdata/eclipse-jdt.metainfo.xml
install -m644 -D desktopintegration/eclipse-pde.metainfo.xml $RPM_BUILD_ROOT%{_datadir}/appdata/eclipse-pde.metainfo.xml

LOCAL_PWD=`pwd`
#change the installation p2 files
pushd eclipse.platform.releng.tychoeclipsebuilder/platform/target/products/org.eclipse.platform.ide/linux/gtk/%{eclipse_arch}/eclipse/p2/org.eclipse.equinox.p2.engine/profileRegistry/SDKProfile.profile/
for i in `ls | grep "profile.gz"` ; do  \
        echo $i ; \
        gunzip $i ; \
        sed -i -e "s@${LOCAL_PWD}/eclipse.platform.releng.tychoeclipsebuilder/platform/target/products/org.eclipse.platform.ide/linux/gtk/%{eclipse_arch}/eclipse@%{_eclipsedir}@g" *.profile ; \
        gzip *.profile ; \
    done 
popd 

#installation itself - copy it into right location
rsync -vrpl eclipse.platform.releng.tychoeclipsebuilder/platform/target/products/org.eclipse.platform.ide/linux/gtk/%{eclipse_arch}/eclipse \
    %{buildroot}%{_prefix}/lib

# Symlink eclipse binary
pushd %{buildroot}%{_bindir}
    ln -s %{_eclipsedir}/eclipse
popd

# Symlink eclipse ini
pushd %{buildroot}/%{_sysconfdir}/
    ln -s %{_eclipsedir}/eclipse.ini
popd

# List jars to be symlinked into javadir
pushd %{buildroot}%{_eclipsedir}/plugins
EQUINOX_JARS=$(ls . | grep -P '^org.eclipse.equinox(?!.*\.ui[\._])' | sed -e 's|^org\.eclipse\.\(.*\)_.*|\1|')
OSGI_JARS=$(ls . | grep '^org.eclipse.osgi' | sed -e 's|^org\.eclipse\.\(.*\)_.*|\1|')
popd

# Symlink jars into javadir
location=%{_eclipsedir}/plugins
while [ "$location" != "/" ] ; do
    location=$(dirname $location)
    updir="$updir../"
done
pushd %{buildroot}%{_javadir}/eclipse
for J in $EQUINOX_JARS core.contenttype core.jobs core.net core.runtime ; do
  DIR=$updir%{_eclipsedir}/plugins
  if [ "$J" != "equinox.http.servlet" ] ; then
    [ -e "`ls $DIR/org.eclipse.${J}_*.jar`" ] && ln -s $DIR/org.eclipse.${J}_*.jar ${J}.jar
  fi
done
popd

# Generate addition Maven metadata
rm -rf .xmvn/ .xmvn-reactor
%mvn_package "org.eclipse.osgi:" equinox-osgi
%mvn_package "org.eclipse.swt:" swt

# Install Maven metadata for OSGi jars
for J in $OSGI_JARS ; do
  JAR=%{buildroot}%{_eclipsedir}/plugins/org.eclipse.${J}_*.jar
  VER=$(echo $JAR | sed -e "s/.*${J}_\(.*\)\.jar/\1/")
  %mvn_artifact "org.eclipse.osgi:$J:jar:$VER" $JAR
  %mvn_alias "org.eclipse.osgi:$J" "org.eclipse.osgi:org.eclipse.$J" "org.eclipse.platform:org.eclipse.$J"
done

# Install Maven metadata for SWT
JAR=%{buildroot}%{_eclipsedir}/plugins/org.eclipse.swt_*.jar
VER=$(echo $JAR | sed -e "s/.*_\(.*\)\.jar/\1/")
%mvn_artifact "org.eclipse.swt:org.eclipse.swt:jar:$VER" ./eclipse.platform.swt.binaries/bundles/org.eclipse.swt.gtk.linux.%{eclipse_arch}/target/org.eclipse.swt.gtk.linux.%{eclipse_arch}-*-SNAPSHOT.jar
%mvn_alias "org.eclipse.swt:org.eclipse.swt" "org.eclipse.swt:swt"
%mvn_file "org.eclipse.swt:org.eclipse.swt" swt

%mvn_install

# Symlink SWT jar
pushd %{buildroot}/%{_eclipsedir}/
    ln -s $(abs2rel %{_jnidir}/swt.jar %{_eclipsedir})
popd

#fix so permissions
find $RPM_BUILD_ROOT/%{_eclipsedir} -name *.so -exec chmod a+x {} \;

# Usage marker
install -d -m 755 %{buildroot}%{_eclipsedir}/.pkgs
echo "%{version}-%{release}" > %{buildroot}%{_eclipsedir}/.pkgs/Distro%{?dist}

%files swt -f .mfiles-swt
%{_eclipsedir}/plugins/org.eclipse.swt_*
%{_eclipsedir}/plugins/org.eclipse.swt.gtk.linux.*
%{_eclipsedir}/swt.jar
%{_jnidir}/swt.jar

%files platform
%{_bindir}/eclipse
%{_eclipsedir}/eclipse
%{_eclipsedir}/.eclipseproduct
%{_eclipsedir}/.pkgs
%config %{_eclipsedir}/eclipse.ini
%config %{_sysconfdir}/eclipse.ini
/usr/share/applications/*
/usr/share/pixmaps/*
/usr/share/icons/*/*/apps/*
%{_datadir}/appdata/eclipse.appdata.xml
%dir %{_eclipsedir}/configuration/
%dir %{_eclipsedir}/configuration/org.eclipse.equinox.simpleconfigurator/
%{_eclipsedir}/configuration/config.ini
%{_eclipsedir}/configuration/org.eclipse.equinox.simpleconfigurator/bundles.info
%{_eclipsedir}/features/org.eclipse.core.runtime.feature_*
%{_eclipsedir}/features/org.eclipse.e4.rcp_*
%{_eclipsedir}/features/org.eclipse.equinox.core.feature_*
%{_eclipsedir}/features/org.eclipse.equinox.p2.core.feature_*
%{_eclipsedir}/features/org.eclipse.equinox.p2.extras.feature_*
%{_eclipsedir}/features/org.eclipse.equinox.p2.rcp.feature_*
%{_eclipsedir}/features/org.eclipse.equinox.p2.user.ui_*
%{_eclipsedir}/features/org.eclipse.help_*
%{_eclipsedir}/features/org.eclipse.platform_*
%{_eclipsedir}/features/org.eclipse.rcp_*
%{_eclipsedir}/plugins/com.ibm.icu_*
%{_eclipsedir}/plugins/com.jcraft.jsch_*
%{_eclipsedir}/plugins/javax.*
%if 0%{?fedora} >= 33 || 0%{?eln}
%{_eclipsedir}/plugins/jakarta.*
%{_eclipsedir}/plugins/org.glassfish.jakarta.el_*
%{_eclipsedir}/plugins/org.glassfish.web.jakarta.servlet.jsp_*
%else
%{_eclipsedir}/plugins/com.sun.el.javax.el_*
%{_eclipsedir}/plugins/org.glassfish.web.javax.servlet.jsp_*
%endif
%{_eclipsedir}/plugins/org.apache.*
%{_eclipsedir}/plugins/org.eclipse.ant.core_*
%{_eclipsedir}/plugins/org.eclipse.compare_*
%{_eclipsedir}/plugins/org.eclipse.compare.core_*
%{_eclipsedir}/plugins/org.eclipse.core.commands_*
%{_eclipsedir}/plugins/org.eclipse.core.contenttype_*
%{_eclipsedir}/plugins/org.eclipse.core.databinding.beans_*
%{_eclipsedir}/plugins/org.eclipse.core.databinding.observable_*
%{_eclipsedir}/plugins/org.eclipse.core.databinding.property_*
%{_eclipsedir}/plugins/org.eclipse.core.databinding_*
%{_eclipsedir}/plugins/org.eclipse.core.expressions_*
%{_eclipsedir}/plugins/org.eclipse.core.externaltools_*
%{_eclipsedir}/plugins/org.eclipse.core.filebuffers_*
%{_eclipsedir}/plugins/org.eclipse.core.filesystem*
%{_eclipsedir}/plugins/org.eclipse.core.jobs_*
%{_eclipsedir}/plugins/org.eclipse.core.net*
%{_eclipsedir}/plugins/org.eclipse.core.resources_*
%{_eclipsedir}/plugins/org.eclipse.core.runtime_*
%{_eclipsedir}/plugins/org.eclipse.core.variables_*
%{_eclipsedir}/plugins/org.eclipse.debug.core_*
%{_eclipsedir}/plugins/org.eclipse.debug.ui_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.commands_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.contexts_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.di_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.di.annotations_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.di.extensions_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.di.extensions.supplier_*
%{_eclipsedir}/plugins/org.eclipse.e4.core.services_*
%{_eclipsedir}/plugins/org.eclipse.e4.emf.xpath_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.bindings_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.css.core_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.css.swt_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.css.swt.theme_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.di_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.dialogs_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.ide_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.model.workbench_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.services_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.swt.gtk_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.widgets_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.workbench_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.workbench3_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.workbench.addons.swt_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.workbench.renderers.swt_*
%{_eclipsedir}/plugins/org.eclipse.e4.ui.workbench.swt_*
%{_eclipsedir}/plugins/org.eclipse.equinox.app_*
%{_eclipsedir}/plugins/org.eclipse.equinox.bidi_*
%{_eclipsedir}/plugins/org.eclipse.equinox.common_*
%{_eclipsedir}/plugins/org.eclipse.equinox.concurrent_*
%{_eclipsedir}/plugins/org.eclipse.equinox.console_*
%{_eclipsedir}/plugins/org.eclipse.equinox.ds_*
%{_eclipsedir}/plugins/org.eclipse.equinox.event_*
%{_eclipsedir}/plugins/org.eclipse.equinox.frameworkadmin_*
%{_eclipsedir}/plugins/org.eclipse.equinox.frameworkadmin.equinox_*
%{_eclipsedir}/plugins/org.eclipse.equinox.http.jetty_*
%{_eclipsedir}/plugins/org.eclipse.equinox.http.registry_*
%{_eclipsedir}/plugins/org.eclipse.equinox.http.servlet_*
%{_eclipsedir}/plugins/org.eclipse.equinox.jsp.jasper_*
%{_eclipsedir}/plugins/org.eclipse.equinox.jsp.jasper.registry_*
%{_eclipsedir}/plugins/org.eclipse.equinox.launcher_*
%{_eclipsedir}/plugins/org.eclipse.equinox.launcher.gtk.linux.*_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.artifact.repository_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.console_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.core_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.director_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.director.app_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.directorywatcher_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.engine_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.extensionlocation_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.garbagecollector_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.jarprocessor_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.metadata_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.metadata.repository_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.operations_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.publisher_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.publisher.eclipse_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.reconciler.dropins_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.repository_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.repository.tools_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.touchpoint.eclipse_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.touchpoint.natives_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.transport.ecf_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.ui_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.ui.importexport_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.ui.sdk_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.ui.sdk.scheduler_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.updatechecker_*
%{_eclipsedir}/plugins/org.eclipse.equinox.p2.updatesite_*
%{_eclipsedir}/plugins/org.eclipse.equinox.preferences_*
%{_eclipsedir}/plugins/org.eclipse.equinox.registry_*
%{_eclipsedir}/plugins/org.eclipse.equinox.security*
%{_eclipsedir}/plugins/org.eclipse.equinox.simpleconfigurator_*
%{_eclipsedir}/plugins/org.eclipse.equinox.simpleconfigurator.manipulator_*
%{_eclipsedir}/plugins/org.eclipse.help_*
%{_eclipsedir}/plugins/org.eclipse.help.base_*
%{_eclipsedir}/plugins/org.eclipse.help.ui_*
%{_eclipsedir}/plugins/org.eclipse.help.webapp_*
%{_eclipsedir}/plugins/org.eclipse.jdt.core.compiler.batch_*
%{_eclipsedir}/plugins/org.eclipse.jetty.*
%{_eclipsedir}/plugins/org.eclipse.jface_*
%{_eclipsedir}/plugins/org.eclipse.jface.databinding_*
%{_eclipsedir}/plugins/org.eclipse.jface.text_*
%{_eclipsedir}/plugins/org.eclipse.jface.notifications_*
%{_eclipsedir}/plugins/org.eclipse.jsch.core_*
%{_eclipsedir}/plugins/org.eclipse.jsch.ui_*
%{_eclipsedir}/plugins/org.eclipse.ltk.core.refactoring_*
%{_eclipsedir}/plugins/org.eclipse.ltk.ui.refactoring_*
%{_eclipsedir}/plugins/org.eclipse.platform_*
%{_eclipsedir}/plugins/org.eclipse.platform.doc.user_*
%{_eclipsedir}/plugins/org.eclipse.rcp_*
%{_eclipsedir}/plugins/org.eclipse.search_*
%{_eclipsedir}/plugins/org.eclipse.team.core_*
%{_eclipsedir}/plugins/org.eclipse.team.genericeditor.diff.extension_*
%{_eclipsedir}/plugins/org.eclipse.team.ui_*
%{_eclipsedir}/plugins/org.eclipse.text_*
%{_eclipsedir}/plugins/org.eclipse.text.quicksearch_*
%{_eclipsedir}/plugins/org.eclipse.ui_*
%{_eclipsedir}/plugins/org.eclipse.ui.browser_*
%{_eclipsedir}/plugins/org.eclipse.ui.cheatsheets_*
%{_eclipsedir}/plugins/org.eclipse.ui.console_*
%{_eclipsedir}/plugins/org.eclipse.ui.editors_*
%{_eclipsedir}/plugins/org.eclipse.ui.externaltools_*
%{_eclipsedir}/plugins/org.eclipse.ui.forms_*
%{_eclipsedir}/plugins/org.eclipse.ui.genericeditor_*
%{_eclipsedir}/plugins/org.eclipse.ui.ide_*
%{_eclipsedir}/plugins/org.eclipse.ui.ide.application_*
%{_eclipsedir}/plugins/org.eclipse.ui.intro_*
%{_eclipsedir}/plugins/org.eclipse.ui.intro.quicklinks_*
%{_eclipsedir}/plugins/org.eclipse.ui.intro.universal_*
%{_eclipsedir}/plugins/org.eclipse.ui.monitoring_*
%{_eclipsedir}/plugins/org.eclipse.ui.navigator_*
%{_eclipsedir}/plugins/org.eclipse.ui.navigator.resources_*
%{_eclipsedir}/plugins/org.eclipse.ui.net_*
%{_eclipsedir}/plugins/org.eclipse.ui.themes_*
%{_eclipsedir}/plugins/org.eclipse.ui.views_*
%{_eclipsedir}/plugins/org.eclipse.ui.views.log_*
%{_eclipsedir}/plugins/org.eclipse.ui.views.properties.tabbed_*
%{_eclipsedir}/plugins/org.eclipse.ui.workbench_*
%{_eclipsedir}/plugins/org.eclipse.ui.workbench.texteditor_*
%{_eclipsedir}/plugins/org.eclipse.update.configurator_*
%{_eclipsedir}/plugins/org.eclipse.urischeme_*
%{_eclipsedir}/plugins/com.sun.jna_*
%{_eclipsedir}/plugins/com.sun.jna.platform_*
%{_eclipsedir}/plugins/org.sat4j.core_*
%{_eclipsedir}/plugins/org.sat4j.pb_*
%{_eclipsedir}/plugins/org.tukaani.xz_*
%{_eclipsedir}/plugins/org.w3c.css.sac_*
%{_eclipsedir}/plugins/org.w3c.dom.svg_*
%doc %{_eclipsedir}/readme
%{_eclipsedir}/artifacts.xml
%{_eclipsedir}/p2
%{_javadir}/%{name}/core*
%{_javadir}/%{name}/equinox*

%files jdt -f .mfiles-jdt
%{_datadir}/appdata/eclipse-jdt.metainfo.xml

%files pde -f .mfiles-pde -f .mfiles-cvs -f .mfiles-sdk
%{_datadir}/appdata/eclipse-pde.metainfo.xml

%files p2-discovery -f .mfiles-p2-discovery

%files equinox-osgi -f .mfiles-equinox-osgi
%{_eclipsedir}/plugins/org.eclipse.osgi_*
%{_eclipsedir}/plugins/org.eclipse.osgi.compatibility.state_*
%{_eclipsedir}/plugins/org.eclipse.osgi.services_*
%{_eclipsedir}/plugins/org.eclipse.osgi.util_*

%changelog
* Wed Nov 18 2020 Mat Booth <mat.booth@redhat.com> - 1:4.17-4
- Drop contributor-tools sub-package
- Remove workaround for old ASM version

* Wed Nov 11 2020 Mat Booth <mat.booth@redhat.com> - 1:4.17-3
- Obsolete usage plugin and ensure encoding in use is UTF-8 during the build

* Fri Nov  6 2020 Mat Booth <mat.booth@redhat.com> - 1:4.17-2
- Fix build on non-intel arches

* Wed Oct 28 2020 Mat Booth - 1:4.17-1
- Update to latest upstream release

* Tue Oct 27 2020 Jie Kang <jkang@redhat.com> - 1:4.16-14
- Update fedora macros to include eln

* Tue Aug 25 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-13
- Platform actually requires OpenJDK devel package for ct.sym

* Mon Aug 24 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-12
- Rebuild against new jakarta-el,-jsp packages
- Fix javadoc generation relying on Windows version of SWT

* Fri Aug 21 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-11
- Rebuild with a dependency on obsolete log4j package
- Run mvn_install with Java 11

* Wed Aug 19 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-10
- Rebuild against jakarta servlet API and updated batik
- Update eclipse-build snapshot

* Fri Aug 14 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-9
- Restore explicit glassfish-annotation-api dep

* Fri Aug 14 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-8
- Rebuild for new jetty version

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-6
- Require Java 11 explicitly
- Drop hotspot exclusions from the JDK 6 era

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:4.16-5
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Jun 29 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-4
- Update linux-build snapshot and fix adding junit classpath containers to java
  projects

* Tue Jun 23 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-3
- Make a bit more portable and fix bootstrap mode

* Fri Jun 19 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-2
- Non-bootstrap build

* Thu Jun 18 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-1
- Update to latest upstream release

* Thu Apr 02 2020 Mat Booth <mat.booth@redhat.com> - 1:4.15-5
- Make the requirement on felix-scr more strict

* Thu Apr 02 2020 Mat Booth <mat.booth@redhat.com> - 1:4.15-4
- Allow library detector to build on Java 11

* Sun Mar 29 2020 Mat Booth <mat.booth@redhat.com> - 1:4.15-3
- Don't build and ship the test framework. We are not shipping any actual tests
  anyway and this allows to drop the dependency on mockito and friends.

* Mon Mar 23 2020 Mat Booth <mat.booth@redhat.com> - 1:4.15-2
- Set compiler release to Java 8 on certain bundles

* Sat Mar 21 2020 Mat Booth <mat.booth@redhat.com> - 1:4.15-1
- Update to latest upstream release

* Tue Jan 28 2020 Mat Booth <mat.booth@redhat.com> - 1:4.14-5
- Backport patch to fix build against GCC 10

* Thu Jan 23 2020 Mat Booth <mat.booth@redhat.com> - 1:4.14-4
- Remove BR on bouncycastle

* Thu Jan 23 2020 Mat Booth <mat.booth@redhat.com> - 1:4.14-3
- Remove references to kxml/xpp3

* Thu Dec 19 2019 Mat Booth <mat.booth@redhat.com> - 1:4.14-2
- Full build
- Drop tests sub-package

* Thu Dec 19 2019 Mat Booth <mat.booth@redhat.com> - 1:4.14-1
- Update to latest upstream release

* Thu Dec 19 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-7
- Bump requirements on EMF/ECF

* Wed Dec 18 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-6
- Remove unnecessary dep on apache-commons-el
- Enable bootstrap mode

* Wed Nov 20 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-5
- Obsolete retired packages

* Mon Sep 23 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-4
- Add patch for ebz#550606

* Mon Sep 23 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-3
- Fix explicit hamcrest reqs

* Mon Sep 16 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-2
- Fix PDE installation

* Mon Sep 09 2019 Mat Booth <mat.booth@redhat.com> - 1:4.13-1
- Update to latest upstream release

* Wed Jul 24 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-6
- Reenable normal debuginfo generation for the launcher binary on Fedora

* Thu Jun 27 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-5
- Fix NoClassDefFoundError regression in ant support

* Thu Jun 20 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-4
- Fix deps on batik stack

* Thu Jun 20 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-3
- Disable more examples and allow contrib-tools mode to build properly

* Wed Jun 19 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-2
- Additional fixes for ebz548211

* Mon Jun 17 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-1
- Update to 2019-06 release

* Sun Jun 16 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-15
- Rebuild against new Jetty, ECF and EMF

* Wed Jun 12 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-14
- Full rebuild

* Wed Jun 12 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-13
- Add patch for lucene 8 and rebootstrap

* Thu May 30 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-12
- Avoid requirement on optional test dependency commons-fileupload

* Fri May 24 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-11
- Clean up unused maven metadata

* Fri May 24 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-10
- Add missing BR on google-gson

* Thu May 23 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-9
- Bump deps on batik and xmlgraphics

* Tue May 07 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-8
- Re-instate junit5 dep since dependent modules were fixed

* Wed May 01 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-7
- Bump requirements on Jetty
- Avoid reliance on Javascript in SWT build

* Tue Apr 30 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-6
- Disable hard requirement on ant-junit5

* Thu Apr 25 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-5
- Fix bootstrap mode to use bcond flags
- Bump requirements on Jetty, SCR and ICU4j

* Wed Apr 10 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-4
- Obsolete recommenders package, rhbz#1698504

* Tue Mar 19 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-3
- Pre-strip debuginfo from the launcher binary to avoid conflicts with other RCP
  applications, which will use identical launcher binaries

* Thu Mar 14 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-2
- Full build

* Mon Mar 11 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-1
- Update to 2019-03 release
- Drop support for 32-bit architectures

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Mat Booth <mat.booth@redhat.com> - 1:4.10.0-2
- No longer recommend Code Recommenders

* Tue Dec 11 2018 Mat Booth <mat.booth@redhat.com> - 1:4.10.0-1
- Update to 2018-12 release
- Update eclipse-build snapshot

* Thu Dec 06 2018 Mat Booth <mat.booth@redhat.com> - 1:4.10.0-0.3
- Update to latest I-build
- Build against latest jetty, mockito packages
- Update requirements on EMF and ECF

* Tue Dec 04 2018 Mat Booth <mat.booth@redhat.com> - 1:4.10.0-0.2
- Allow building on Fedora 29

* Thu Nov 29 2018 Mat Booth <mat.booth@redhat.com> - 1:4.10.0-0.1
- Update to latest I-build
- Enable bootstrap mode

* Fri Sep 28 2018 Jeff Johnston <jjohnstn@redhat.com> - 1:4.9.0-2
- Add org.eclipse.equinox.executable for building RCP apps

* Wed Sep 12 2018 Mat Booth <mat.booth@redhat.com> - 1:4.9.0-1
- Update to final bits for 4.9
- Fix NPE due to missing agent jar

* Thu Aug 23 2018 Mat Booth <mat.booth@redhat.com> - 1:4.9.0-0.4
- Update to latest I-build
- Full non-bootstrap build

* Wed Aug 22 2018 Mat Booth <mat.booth@redhat.com> - 1:4.9.0-0.3
- Fix prefer x11 patch used on RHEL

* Mon Aug 20 2018 Mat Booth <mat.booth@redhat.com> - 1:4.9.0-0.2
- Fix secondary arch build

* Sun Aug 19 2018 Mat Booth <mat.booth@redhat.com> - 1:4.9.0-0.1
- Update to latest I-build
- Update license

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-3
- Add patch to use gsettings instead of gconf

* Wed Jun 13 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-2
- Backport patches for ebz#533655 and ebz#535392

* Tue Jun 12 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-1
- Update to Photon release

* Thu Jun 07 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.8
- Update to last RC of Photon

* Mon May 21 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.7
- Updated I-build
- Switch to using upstream tarball
- Disable unused annotation bundle

* Mon May 21 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.6
- Rebuild to correct permissions

* Tue May 15 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.5
- Rebuild against Photon EMF and ECF versions
- Updated I-build

* Thu May 03 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.4
- Updated I-build
- Attempt to fix arm platform launchers

* Wed May 02 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.3
- Non-bootstrap build

* Sat Apr 28 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.2
- Update to latest I-build and fix build on 32bit intel platform
- Tighten deps on batik to prevent runtime bundle resolution errors

* Tue Apr 24 2018 Mat Booth <mat.booth@redhat.com> - 1:4.8.0-0.1
- Update to Photon I-build
- Remove conditional for webkit2 (always use it now)
- Bump requirement on lucene

* Tue Apr 10 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3a-4
- Ensure patches apply cleanly
- Use java API stubs from ecj package

* Mon Apr 09 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3a-3
- Package java 10 API stubs jar

* Mon Apr 09 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3a-2
- Backport patches to fix broken table editing

* Mon Apr 09 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3a-1
- Update to Oxygen.3a release for java 10 support

* Wed Mar 21 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3-2
- Bump jetty dependency

* Thu Mar 15 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3-1
- Update to Oxygen.3 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Merlin Mathesius <mmathesi@redhat.com> - 1:4.7.2-2
- Cleanup spec file conditionals

* Wed Nov 29 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.2-1
- Update to last RC/final release of Oxygen.2
- Fix x11 crash when running on wayland

* Fri Nov 24 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.2-0.2
- Update to latest RC of Oxygen.2

* Tue Nov 21 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.2-0.1
- Update to latest RC of Oxygen.2

* Fri Nov 17 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-8
- Make java 9 api stubs available for use
- Migrate away from deprecated maven depmap macros

* Wed Oct 18 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-7
- Update to 4.7.1a release

* Mon Oct 02 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-6
- Use the jit on 32bit arm to speed up the build

* Mon Oct 02 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-5
- Drop workaround for metainfo problem
- Add patch for javascript/webkit2 bug ebz#525340
- Add missing mocking deps for contributor-tools

* Tue Sep 19 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-4
- Add workaround for appstream metainfo bug in RPM on F27

* Tue Sep 19 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-3
- Obsolete e4-importer that was moved into platform
- Add recommends on recommenders from JDT

* Fri Sep 15 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-2
- Debootstrap build

* Fri Sep 15 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-1
- Update to Oxygen.1 release
- Relax restriction on objectweb-asm

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 04 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-2
- Use 'protect root' instead of 'protect master'

* Fri Jun 30 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-1
- Update to final Oxygen release
- Bump jetty requirement

* Thu Jun 15 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.14
- Update to latest release candidate build
- Rebuild for latest EMF and ECF
- Drop nashorn extension mechanism

* Wed May 31 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:4.7.0-0.13
- Add missing build-requires on Maven plugins
- Run xmvn in batch mode

* Thu May 18 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.12
- Enable Wayland backend by default on F27+
- Bump some dependency requirements

* Tue May 16 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.11
- Update to latest I-build
- Rebuild for latest EMF

* Tue May 09 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.10
- Rebuild for new ECF
- Obsolete core NLS package
- Fix cycle introduced between tests and contributor-tools

* Sat May 06 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.9
- Fix build against new felix-gogo
- Update to latest I-build

* Wed May 03 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.8
- Package missing PDE generic editor extension

* Tue May 02 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.7
- Rebuild for s390x
- Don't require JDK directly

* Fri Apr 28 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.6
- Non-bootstrap build

* Tue Apr 25 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.5
- Update to latest I-build
- Update generated ant bundle to 1.10.1
- Fix missing launcher bundle on s390, rhbz#1445162
- Add missing BR on libsecret

* Fri Apr 21 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.4
- Fix secondary arch build

* Thu Apr 20 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.3
- Simplify test installation and move machinery out of javadir now
  that java stuff is installed in its own place
- Enable bootstrap mode

* Wed Apr 19 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.2
- Update to latest I-build

* Tue Apr 04 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.0-0.1
- Update to Oxygen I-build
- Don't build unsupported GTK2 backend for SWT
- Move installation to a multilib agnostic location /usr/lib

