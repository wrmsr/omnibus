from .. import maven as mvn


PREAMBLE = {
    'modelVersion': '4.0.0',

    'groupId': 'com.wrmsr.tokamak',
    'artifactId': 'tokamak-parent',
    'version': '0.1-SNAPSHOT',
    'packaging': 'jar',
}


PROPERTIES = {
    'project.build.sourceEncoding': 'UTF-8',

    'main.basedir': '${project.basedir}',

    'protobuf.input.directory': '${project.basedir}/src/main/proto',
    'protobuf.output.directory': '${project.build.directory}/generated-sources',

    'dep.antlr4.version': '4.8-1',
    'dep.guice.version': '4.2.2',
    'dep.jackson.version': '2.11.0',
    'dep.jersey.version': '2.30.1',
    'dep.protobuf.version': '3.11.4',
}


DEPENDENCIES = [

    mvn.Dependency('com.google.protobuf', 'protobuf-java', '${dep.protobuf.version}'),

    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-annotations', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-core', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-databind', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-module-parameter-names', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-module-afterburner', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-datatype-jdk8', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-datatype-jsr310', '${dep.jackson.version}'),
    mvn.Dependency(
        'com.fasterxml.jackson.core',
        'jackson-datatype-guava',
        '${dep.jackson.version}',
        exclusions=[
            mvn.Exclusion('com.google.guava', 'guava'),
        ],
    ),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-dataformat-yaml', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-dataformat-cbor', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-dataformat-smile', '${dep.jackson.version}'),
    mvn.Dependency('com.fasterxml.jackson.core', 'jackson-dataformat-csv', '${dep.jackson.version}'),

    mvn.Dependency('org.apache.logging.log4j', 'log4j-core', '2.13.2'),
    mvn.Dependency('org.apache.logging.log4j', 'log4j-slf4j-impl', '2.13.2'),
    mvn.Dependency('org.apache.logging.log4j', 'log4j-jul', '2.13.2'),
    mvn.Dependency('org.apache.logging.log4j', 'log4j-web', '2.13.2'),

    mvn.Dependency('com.google.guava', 'guava', '29.0-jre'),
    mvn.Dependency('javax.annotation', 'javax.annotation-api', '1.3.2'),

    mvn.Dependency('mysql', 'mysql-connector-java', '8.0.20'),
    mvn.Dependency('org.mariadb.jdbc', 'mariadb-java-client', '2.6.0'),
    mvn.Dependency('org.postgresql', 'postgresql', '42.2.12'),

    mvn.Dependency('com.eclipsesource.j2v8', 'j2v8_macosx_x86_64', '4.6.0'),
    mvn.Dependency('org.mozilla', 'rhino', '1.7.12'),

    mvn.Dependency(
        'org.apache.spark',
        'spark-core_2.11a',
        '2.4.5',
        exclusions=[
            mvn.Exclusion('org.slf4j', 'jul-to-slf4j'),
        ],
    ),
    mvn.Dependency('com.fasterxml.jackson.module', 'jackson-module-scala_2.11', '${dep.jackson.version}'),

    mvn.Dependency('com.tdunning', 't-digest', '3.2'),
    mvn.Dependency('org.hdrhistogram', 'HdrHistogram', '2.1.12'),
    mvn.Dependency('io.lacuna', 'bifurcan', '0.1.0'),
    mvn.Dependency('it.unimi.dsi', 'fastutil', '8.3.1'),
    mvn.Dependency('com.netopyr.wurmloch', 'wurmloch-crdt', '0.1.0'),
    mvn.Dependency('it.unimi.dsi', 'sux4j', '5.0.4'),
    mvn.Dependency('com.clearspring.analytics', 'stream', '2.9.8'),

    mvn.Dependency('com.kohlschutter.junixsocket', 'junixsocket-common', '2.3.2'),
    mvn.Dependency('com.kohlschutter.junixsocket', 'junixsocket-native-common', '2.3.2'),

    mvn.Dependency('org.rocksdb', 'rocksdbjni', '6.7.3'),
    mvn.Dependency('com.h2database', 'h2', '1.4.200'),
    mvn.Dependency('org.xerial', 'sqlite-jdbc', '3.30.1'),

    mvn.Dependency('org.slf4j', 'slf4j-jdk14', '1.7.30'),

    mvn.Dependency('io.airlift', 'aircompressor', '0.16'),
    mvn.Dependency('org.xerial.snappy', 'snappy-java', '1.1.7.3'),
    mvn.Dependency('com.github.luben', 'zstd-jni', '1.4.4-9'),

    mvn.Dependency('org.sonatype.aether', 'aether-api', '1.13.1'),
    mvn.Dependency('io.airlift.resolver', 'resolver', '1.6'),

    mvn.Dependency('org.apache.commons', 'commons-math3', '3.6.1'),

    mvn.Dependency(
        'org.apache.kafka',
        'kafka_2.11a',
        '2.4.1',
        exclusions=[
            mvn.Exclusion('log4j', 'log4j'),
            mvn.Exclusion('org.slf4j', 'slf4j-log4j12j'),
        ],
    ),

    mvn.Dependency(
        'org.apache.zookeeper',
        'zookeeper',
        '3.6.0',
        exclusions=[
            mvn.Exclusion('jline', 'jline'),
            mvn.Exclusion('log4j', 'log4j'),
            mvn.Exclusion('org.slf4j', 'slf4j-log4j12'),
        ]
    ),

    mvn.Dependency('com.teradata', 're2j-td', '1.4'),

    mvn.Dependency('com.esotericsoftware', 'kryo', '5.0.0-RC5'),

    mvn.Dependency('org.apache.maven.plugins', 'maven-dependency-plugin', '3.1.2'),

    mvn.Dependency('junit', 'junit', '4.13', scope=mvn.Scope.TEST),

]


PLUGINS = [

    mvn.Plugin(
        'org.apache.maven.plugins',
        'maven-compiler-plugin',
        '3.8.1',
        configuration={
            'source': '1.8',
            'target': '1.8',
            'encoding': 'UTF-8',
            'compilerArgs': [
                {'arg': '-Xlint:all,-options,-path'},
                {'arg': '-parameters'},
                {'arg': '-g'},
            ],
        },
    ),

    mvn.Plugin('org.codehaus.mojo', 'versions-maven-plugin', '2.7'),

    mvn.Plugin('org.apache.maven.plugins', 'maven-shade-plugin', '3.2.1'),

    mvn.Plugin(
        'org.apache.maven.plugins',
        'maven-assembly-plugin',
        '2.4',
        configuration={
            'appendAssemblyId': 'true',
            'tarLongFileMode': 'gnu',
        },
    ),

    mvn.Plugin(
        'org.antlr',
        'antlr4-maven-plugin',
        '${dep.antlr4.version}',
        configuration={
            'visitor': 'true',
        },
        executions=[
            mvn.Execution([mvn.Goal('antlr4')])
        ],
    ),

    mvn.Plugin('exec-maven-plugin', 'org.codehaus.mojo', '1.6.0'),

    mvn.Plugin('org.apache.maven.plugins', 'maven-antrun-plugin', '1.8'),

    mvn.Plugin('org.apache.maven.plugins', 'maven-jar-plugin', '3.1.2'),

    mvn.Plugin('com.github.jinnovations', 'attribution-maven-plugin', '0.9.5'),

]


def test_maven():
    prj = mvn.Project(
        PREAMBLE,
        PROPERTIES,
        DEPENDENCIES,
        PLUGINS,
    )

    root = mvn.build_project_tree(prj)

    print(mvn.prettify(root))
