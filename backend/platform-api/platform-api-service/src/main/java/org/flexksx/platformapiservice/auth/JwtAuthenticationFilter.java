package org.flexksx.platformapiservice.auth;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import lombok.RequiredArgsConstructor;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.flexksx.platformapiservice.user.persistence.UserRepository;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

  private final JwtService jwtService;
  private final UserRepository userRepository;

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {

    String authHeader = request.getHeader("Authorization");
    if (authHeader == null || !authHeader.startsWith("Bearer ")) {
      chain.doFilter(request, response);
      return;
    }

    String token = authHeader.substring(7);
    try {
      Claims claims = jwtService.parse(token);
      String userId = claims.getSubject();
      Integer tokenVersion = claims.get("token_version", Integer.class);

      UserEntity user = userRepository.findById(userId).orElse(null);
      if (user == null || !user.getTokenVersion().equals(tokenVersion)) {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        return;
      }

      UserPrincipal principal = new UserPrincipal(user);
      UsernamePasswordAuthenticationToken auth =
          new UsernamePasswordAuthenticationToken(principal, null, principal.getAuthorities());
      SecurityContextHolder.getContext().setAuthentication(auth);

    } catch (JwtException e) {
      response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
      return;
    }

    chain.doFilter(request, response);
  }
}
