package org.flexksx.platformapiservice.auth;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import javax.crypto.SecretKey;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class JwtService {

  private static final String TOKEN_VERSION_CLAIM = "token_version";

  @Value("${jwt.secret}")
  private String secret;

  @Value("${jwt.expiration-ms}")
  private long expirationMs;

  public String issue(UserEntity user) {
    return Jwts.builder()
        .subject(user.getId())
        .claim(TOKEN_VERSION_CLAIM, user.getTokenVersion())
        .issuedAt(new Date())
        .expiration(new Date(System.currentTimeMillis() + expirationMs))
        .signWith(signingKey())
        .compact();
  }

  public Claims parse(String token) throws JwtException {
    return Jwts.parser().verifyWith(signingKey()).build().parseSignedClaims(token).getPayload();
  }

  private static final int HS256_MIN_KEY_BYTES = 32;

  private SecretKey signingKey() {
    return Keys.hmacShaKeyFor(resolveHmacKeyBytes());
  }

  private byte[] resolveHmacKeyBytes() {
    String s = secret.trim();
    try {
      byte[] decoded = Decoders.BASE64.decode(s);
      if (decoded.length >= HS256_MIN_KEY_BYTES) {
        return decoded;
      }
    } catch (Exception e) {
      // DecodingException may wrap checked IO; invalid base64 or too-short decoded use UTF-8
    }
    return requireKeyLength(
        s.getBytes(StandardCharsets.UTF_8),
        "need Base64(≥32 decoded bytes) or ≥32 UTF-8 bytes; e.g. openssl rand -base64 32");
  }

  private static byte[] requireKeyLength(byte[] key, String problem) {
    if (key.length < HS256_MIN_KEY_BYTES) {
      throw new IllegalStateException("jwt.secret: " + problem);
    }
    return key;
  }
}
