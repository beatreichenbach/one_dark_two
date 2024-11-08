import org.jetbrains.changelog.Changelog
import org.jetbrains.changelog.date
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

fun properties(key: String) = project.findProperty(key).toString()

plugins {
  // Java support
  id("java")
  // Kotlin support
  id("org.jetbrains.kotlin.jvm") version "2.0.21"
  // Gradle IntelliJ Plugin
  id("org.jetbrains.intellij.platform") version "2.1.0"
  // Gradle Changelog Plugin
  id("org.jetbrains.changelog") version "2.2.1"
}

group = properties("pluginGroup")
version = properties("pluginVersion")

// Configure project's dependencies
repositories {
  mavenCentral()
  intellijPlatform {
    defaultRepositories()
  }
}

dependencies {
  intellijPlatform {
    create(properties("platformType"), properties("platformVersion"))
    instrumentationTools()
  }
}

// Configure Gradle IntelliJ Plugin - read more: https://github.com/JetBrains/gradle-intellij-plugin
intellijPlatform {
  pluginConfiguration {
    name = properties("pluginName")
    ideaVersion {
      sinceBuild = properties("pluginSinceBuild")
      untilBuild = provider { null }
    }
  }
}

// Configure Gradle Changelog Plugin - read more: https://github.com/JetBrains/gradle-changelog-plugin
changelog {
  version.set(properties("pluginVersion"))
  path.set(file("CHANGELOG.md").canonicalPath)
  header.set(provider { "${version.get()} - ${date()}"})
  headerParserRegex.set("""(\d\.\d\.\d)""".toRegex())
  itemPrefix.set("-")
  keepUnreleasedSection.set(true)
  unreleasedTerm.set("[Unreleased]")
  groups.set(listOf("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"))
}

kotlin {
    compilerOptions {
        apiVersion.set(org.jetbrains.kotlin.gradle.dsl.KotlinVersion.KOTLIN_1_9)
    }
}

tasks {
  wrapper {
    gradleVersion = properties("gradleVersion")
  }

  patchPluginXml {
    // Get the latest available change notes from the changelog file
    changeNotes.set(provider {
      changelog.renderItem(changelog.getLatest(), Changelog.OutputType.HTML)
    })
  }

  signPlugin {
    certificateChain.set(System.getenv("CERTIFICATE_CHAIN"))
    privateKey.set(System.getenv("PRIVATE_KEY"))
    password.set(System.getenv("PRIVATE_KEY_PASSWORD"))
  }

  publishPlugin {
    dependsOn("patchChangelog")
    token.set(System.getenv("PUBLISH_TOKEN"))
    channels.set(listOf("default"))
  }
}

tasks.buildSearchableOptions {
  enabled = false
}
