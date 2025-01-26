use anyhow::Result;

pub(crate) fn foo() -> Result<i32> {
    if true {
        Ok(1)
    } else {
        Err(anyhow::anyhow!("error"))
    }
}
