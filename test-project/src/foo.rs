use anyhow::Result;

pub(crate) fn foo() -> Result<i32> {
    if true {
        Ok(42)
    } else {
        Err(anyhow::anyhow!("error"))
    }
}
