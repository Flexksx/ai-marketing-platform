package org.flexksx.platformapiservice.brandaccess.persistence;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BrandAccessRepository extends JpaRepository<BrandAccessEntity, String> {

  List<BrandAccessEntity> findAllByBrandId(String brandId);

  Optional<BrandAccessEntity> findByUserIdAndBrandId(String userId, String brandId);

  boolean existsByUserIdAndBrandId(String userId, String brandId);
}
