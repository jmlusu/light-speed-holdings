import { describe, it, expect } from 'vitest';
import { colors } from './colors';

describe('colors tokens', () => {
  it('has brand colors', () => {
    expect(colors.navy).toBe('#070A40');
    expect(colors.red).toBe('#E63946');
    expect(colors.cyan).toBe('#00BFFF');
    expect(colors.morningMist).toBe('#F7F8F9');
    expect(colors.deepMineral).toBe('#121518');
    expect(colors.white).toBe('#FFFFFF');
  });

  it('has semantic light colors', () => {
    expect(colors.light.bgPrimary).toBe('#F7F8F9');
    expect(colors.light.textPrimary).toBe('#070A40');
    expect(colors.light.borderFocus).toBe('#00BFFF');
  });

  it('has semantic dark colors', () => {
    expect(colors.dark.bgPrimary).toBe('#121518');
    expect(colors.dark.textPrimary).toBe('#FFFFFF');
    expect(colors.dark.borderFocus).toBe('#00BFFF');
  });

  it('has honesty badge colors', () => {
    expect(colors.honesty.proven.text).toBe('#00BFFF');
    expect(colors.honesty.pilot.text).toBe('#E63946');
  });
});
