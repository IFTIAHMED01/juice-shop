import { describe, it, expect } from 'vitest'
import * as utils from '../../lib/utils'

describe('Independent Unit Tests - Juice Shop Utility Functions', () => {
  //For 1st Test Case of Unit Testing

  it('UT-01: should return a successful response by default', () => {
    const result = utils.queryResultToJson([])

    expect(result).toEqual({
      status: 'success',
      data: []
    })
  })
  //For 2nd Test Case of Unit Testing

  it('UT-02: should identify a valid HTTP URL', () => {
    const result = utils.isUrl('https://example.com')

    expect(result).toBe(true)
  })
//For 3rd Test Case of Unit Testing

it('UT-03: should reject a non-HTTP URL', () => {
  const result = utils.isUrl('ftp://example.com')

  expect(result).toBe(false)
})
//For 4th Test Case of Unit Testing

it('UT-04: should remove quotation marks from a quoted string', () => {
  const result = utils.unquote('"Hello World"')

  expect(result).toBe('Hello World')
})
//For 5th Test Case of Unit Testing

it('UT-05: should truncate a string exceeding the specified length', () => {
  const result = utils.trunc('Hello World', 5)

  expect(result).toBe('Hell...')
})
//For 6th Test Case of Unit Testing

it('UT-06: should format month and day with leading zeros', () => {
  const result = utils.toISO8601(new Date('2025-03-05T00:00:00Z'))

  expect(result).toBe('2025-03-05')
})
//For 7th Test Case of Unit Testing

it('UT-07: should extract a URL-encoded filename with query parameters', () => {
  const result = utils.extractFilename(
    'https://example.com/files/my%20document.pdf?download=true'
  )

  expect(result).toBe('my document.pdf')
})
//For 8th Test Case of Unit Testing

it('UT-08: should convert an IPv4-mapped IPv6 address to IPv4', () => {
  const result = utils.toSimpleIpAddress('::ffff:192.168.1.10')

  expect(result).toBe('192.168.1.10')
})

})
