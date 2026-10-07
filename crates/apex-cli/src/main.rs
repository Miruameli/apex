//! apex CLI entry point.
//!
//! Bare invocation launches the TUI (phase 3); until then it prints help.

use clap::{Parser, Subcommand};

/// Apex terminal AI coding agent.
#[derive(Parser)]
#[command(name = "apex", version, about)]
struct Cli {
    #[command(subcommand)]
    command: Option<Command>,
}

#[derive(Subcommand)]
enum Command {
    /// Start an interactive chat session.
    Chat,
    /// Review code changes for security and clean code.
    Review { path: String },
    /// Show codebase context index.
    Context,
    /// Commit changes with a message.
    Commit { message: String },
    /// Ship / release the current work.
    Ship { message: String },
    /// Skill management: add, list, run, validate.
    Skill {
        #[command(subcommand)]
        subcommand: SkillSubcommand,
    },
    /// Initialize a new Apex project.
    Init,
    /// Configure Apex settings.
    Config {
        #[arg(short, long)]
        setting: Option<String>,
        #[arg(short, long, value_name = "VALUE")]
        value: Option<String>,
    },
}

#[derive(Subcommand)]
enum SkillSubcommand {
    /// Add a new skill.
    Add { name: String },
    /// List available skills.
    List,
    /// Run a skill by name.
    Run { name: String },
    /// Validate a skill.
    Validate { name: String },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Some(Command::Chat) => eprintln!("apex chat: not implemented yet (phase 2)"),
        Some(Command::Review { path }) => {
            eprintln!("apex review {path}: not implemented yet")
        }
        Some(Command::Context) => eprintln!("apex context: not implemented yet"),
        Some(Command::Commit { message }) => {
            eprintln!("apex commit {message}: not implemented yet")
        }
        Some(Command::Ship { message }) => {
            eprintln!("apex ship {message}: not implemented yet")
        }
        Some(Command::Skill { subcommand }) => match subcommand {
            SkillSubcommand::Add { name } => {
                eprintln!("apex skill add {name}: not implemented yet")
            }
            SkillSubcommand::List => eprintln!("apex skill list: not implemented yet"),
            SkillSubcommand::Run { name } => {
                eprintln!("apex skill run {name}: not implemented yet")
            }
            SkillSubcommand::Validate { name } => {
                eprintln!("apex skill validate {name}: not implemented yet")
            }
        },
        Some(Command::Init) => eprintln!("apex init: not implemented yet (phase 2)"),
        Some(Command::Config {
            setting,
            value: _value,
        }) => {
            eprintln!(
                "apex config {}: not implemented yet",
                setting.unwrap_or_else(|| "unset".to_string())
            )
        }
        None => eprintln!("apex TUI: not implemented yet (phase 3). Try `apex --help`."),
    }
}
