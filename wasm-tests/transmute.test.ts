import * as assert from  'node:assert/strict';
import * as fs from 'fs/promises';
import * as path from 'path';
import { describe, test } from 'node:test';
import * as cdk_from_cfn from 'cdk-from-cfn';

describe('with sqs template', async () => {
  // GIVEN
  const tpl = await loadTemplate('sqs-template.json');

  test('doing a simple transmute', async () => {
    // WHEN
    const output = cdk_from_cfn.transmute(tpl, 'typescript', 'SqsStack');

    // THEN - no exception
  });

  test('transmute with stack_type=stack (default)', async () => {
    // WHEN
    const output = cdk_from_cfn.transmute(tpl, 'typescript', 'SqsStack', 'stack');

    // THEN - generates cdk.Stack based code
    assert.ok(output.includes('extends cdk.Stack'));
    assert.ok(output.includes('scope: cdk.App'));
    assert.ok(!output.includes("import { Construct } from 'constructs'"));
  });

  test('transmute with stack_type=construct', async () => {
    // WHEN
    const output = cdk_from_cfn.transmute(tpl, 'typescript', 'SqsStack', 'construct');

    // THEN - generates Construct based code
    assert.ok(output.includes('extends Construct'));
    assert.ok(output.includes('scope: Construct'));
    assert.ok(output.includes("import { Construct } from 'constructs'"));
    assert.ok(!output.includes('extends cdk.Stack'));
  });

  test('exception, not panic: unsupported language', async () => {
    // WHEN
    assert.throws(() =>  {
      cdk_from_cfn.transmute(tpl, 'rust', 'SqsStack');
    }, /not a supported language/);
  });
});

test('exception, not panic: cyclic references', async () => {
  // GIVEN
  const tpl = await loadTemplate('cyclic-references.json');

  // WHEN
  assert.throws(() =>  {
    cdk_from_cfn.transmute(tpl, 'typescript', 'SqsStack');
  }, /cyclic references/);
});

test('exception, not panic: invalid reference', async () => {
  // GIVEN
  const tpl = await loadTemplate('invalid-reference.json');

  // WHEN
  assert.throws(() =>  {
    cdk_from_cfn.transmute(tpl, 'typescript', 'SqsStack');
  }, /reference to an unknown logical id/);
});

async function loadTemplate(name: string) {
  return await fs.readFile(path.join(__dirname, name), 'utf-8');
}