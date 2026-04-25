package org.flexksx.platformapiclientstarter;

import org.flexksx.platformapiclient.auth.AuthApi;
import org.flexksx.platformapiclient.brand.BrandApi;
import org.flexksx.platformapiclient.brand.content.BrandContentApi;
import org.flexksx.platformapiclient.brand.member.BrandMemberApi;
import org.flexksx.platformapiclient.user.UserApi;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.support.RestClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

@AutoConfiguration
@EnableConfigurationProperties(PlatformApiClientProperties.class)
public class PlatformApiClientAutoConfiguration {

  @Bean
  @ConditionalOnMissingBean
  public RestClient platformApiRestClient(PlatformApiClientProperties properties) {
    return RestClient.builder().baseUrl(properties.baseUrl()).build();
  }

  @Bean
  @ConditionalOnMissingBean
  public HttpServiceProxyFactory platformApiProxyFactory(RestClient restClient) {
    return HttpServiceProxyFactory.builderFor(RestClientAdapter.create(restClient)).build();
  }

  @Bean
  @ConditionalOnMissingBean
  public AuthApi authApi(HttpServiceProxyFactory factory) {
    return factory.createClient(AuthApi.class);
  }

  @Bean
  @ConditionalOnMissingBean
  public UserApi userApi(HttpServiceProxyFactory factory) {
    return factory.createClient(UserApi.class);
  }

  @Bean
  @ConditionalOnMissingBean
  public BrandApi brandApi(HttpServiceProxyFactory factory) {
    return factory.createClient(BrandApi.class);
  }

  @Bean
  @ConditionalOnMissingBean
  public BrandContentApi brandContentApi(HttpServiceProxyFactory factory) {
    return factory.createClient(BrandContentApi.class);
  }

  @Bean
  @ConditionalOnMissingBean
  public BrandMemberApi brandMemberApi(HttpServiceProxyFactory factory) {
    return factory.createClient(BrandMemberApi.class);
  }
}
