pub mod conditions;
pub mod reference;

trait Instruction {
    fn synthesize() -> String;
}
