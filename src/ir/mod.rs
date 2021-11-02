pub mod conditions;

trait Instruction {
    fn synthesize() -> String;
}
