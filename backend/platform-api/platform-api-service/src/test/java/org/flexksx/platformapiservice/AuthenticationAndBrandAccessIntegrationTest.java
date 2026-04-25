package org.flexksx.platformapiservice;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import org.flexksx.platformapiclient.auth.LoginRequest;
import org.flexksx.platformapiclient.auth.LoginResponse;
import org.flexksx.platformapiclient.brand.BrandResponse;
import org.flexksx.platformapiservice.brand.persistence.BrandEntity;
import org.flexksx.platformapiservice.brand.persistence.BrandRepository;
import org.flexksx.platformapiservice.brandaccess.persistence.BrandAccessEntity;
import org.flexksx.platformapiservice.brandaccess.persistence.BrandAccessRepository;
import org.flexksx.platformapiservice.brandaccess.service.BrandMemberRole;
import org.flexksx.platformapiservice.user.persistence.UserEntity;
import org.flexksx.platformapiservice.user.persistence.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class AuthenticationAndBrandAccessIntegrationTest {

  @Autowired private MockMvc mockMvc;

  @Autowired private UserRepository userRepository;

  @Autowired private BrandRepository brandRepository;

  @Autowired private BrandAccessRepository brandAccessRepository;

  @Autowired private PasswordEncoder passwordEncoder;

  @Autowired private ObjectMapper objectMapper;

  private UserEntity userA;
  private UserEntity userB;
  private BrandEntity brandA;

  @BeforeEach
  void setUp() {
    brandAccessRepository.deleteAll();
    brandRepository.deleteAll();
    userRepository.deleteAll();

    userA = userRepository.save(UserEntity.create("user.a@example.com", passwordEncoder.encode("passwordA")));
    userB = userRepository.save(UserEntity.create("user.b@example.com", passwordEncoder.encode("passwordB")));

    brandA = brandRepository.save(new BrandEntity(null, "Brand A", "http://logo.a", "http://brand.a"));
    brandAccessRepository.save(BrandAccessEntity.of(userA.getId(), brandA.getId(), BrandMemberRole.OWNER));
  }

  @Test
  void testAuthenticationSuccess() throws Exception {
    LoginRequest loginRequest = new LoginRequest("user.a@example.com", "passwordA");

    MvcResult result = mockMvc.perform(post("/auth/login")
            .contentType(MediaType.APPLICATION_JSON)
            .content(objectMapper.writeValueAsString(loginRequest)))
        .andExpect(status().isOk())
        .andReturn();

    String content = result.getResponse().getContentAsString();
    LoginResponse loginResponse = objectMapper.readValue(content, LoginResponse.class);

    assertThat(loginResponse.token()).isNotBlank();
  }

  @Test
  void testAuthenticationFailure() throws Exception {
    LoginRequest loginRequest = new LoginRequest("user.a@example.com", "wrongpassword");

    mockMvc.perform(post("/auth/login")
            .contentType(MediaType.APPLICATION_JSON)
            .content(objectMapper.writeValueAsString(loginRequest)))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void testBrandAccessScope() throws Exception {
    // 1. Authenticate as User A
    String tokenA = login("user.a@example.com", "passwordA");

    // User A can see Brand A
    mockMvc.perform(get("/brands/" + brandA.getId())
            .header("Authorization", "Bearer " + tokenA))
        .andExpect(status().isOk());

    // 2. Authenticate as User B
    String tokenB = login("user.b@example.com", "passwordB");

    // User B CANNOT see Brand A (expect 404 based on BrandService implementation)
    mockMvc.perform(get("/brands/" + brandA.getId())
            .header("Authorization", "Bearer " + tokenB))
        .andExpect(status().isNotFound());

    // 3. Search brands
    // User A search should return Brand A
    MvcResult searchA = mockMvc.perform(get("/brands")
            .header("Authorization", "Bearer " + tokenA))
        .andExpect(status().isOk())
        .andReturn();

    List<BrandResponse> brandsA = objectMapper.readValue(
        searchA.getResponse().getContentAsString(),
        objectMapper.getTypeFactory().constructCollectionType(List.class, BrandResponse.class));
    assertThat(brandsA).extracting(BrandResponse::id).contains(brandA.getId());

    // User B search should return EMPTY list
    MvcResult searchB = mockMvc.perform(get("/brands")
            .header("Authorization", "Bearer " + tokenB))
        .andExpect(status().isOk())
        .andReturn();

    List<BrandResponse> brandsB = objectMapper.readValue(
        searchB.getResponse().getContentAsString(),
        objectMapper.getTypeFactory().constructCollectionType(List.class, BrandResponse.class));
    assertThat(brandsB).isEmpty();
  }

  @Test
  void testUnauthorizedAccess() throws Exception {
    mockMvc.perform(get("/brands"))
        .andExpect(status().isForbidden());
  }

  private String login(String email, String password) throws Exception {
    LoginRequest loginRequest = new LoginRequest(email, password);
    MvcResult result = mockMvc.perform(post("/auth/login")
            .contentType(MediaType.APPLICATION_JSON)
            .content(objectMapper.writeValueAsString(loginRequest)))
        .andExpect(status().isOk())
        .andReturn();

    return objectMapper.readValue(result.getResponse().getContentAsString(), LoginResponse.class).token();
  }
}
