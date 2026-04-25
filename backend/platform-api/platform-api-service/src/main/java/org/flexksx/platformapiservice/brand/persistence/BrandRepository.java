package org.flexksx.platformapiservice.brand.persistence;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface BrandRepository extends JpaRepository<BrandEntity, String> {

  @Query(
      "SELECT b FROM BrandEntity b, BrandAccessEntity m"
          + " WHERE b.id = m.brandId AND m.userId = :userId")
  List<BrandEntity> findAllByUserId(@Param("userId") String userId);

  @Query(
      "SELECT b FROM BrandEntity b, BrandAccessEntity m"
          + " WHERE b.id = m.brandId AND b.id = :brandId AND m.userId = :userId")
  Optional<BrandEntity> findByIdAndUserId(
      @Param("brandId") String brandId, @Param("userId") String userId);
}
