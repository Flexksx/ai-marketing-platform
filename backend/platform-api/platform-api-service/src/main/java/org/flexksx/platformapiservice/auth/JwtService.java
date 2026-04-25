package org.flexksx.platformapiservice.auth;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
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

  private SecretKey signingKey() {
    return Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
  }
}
