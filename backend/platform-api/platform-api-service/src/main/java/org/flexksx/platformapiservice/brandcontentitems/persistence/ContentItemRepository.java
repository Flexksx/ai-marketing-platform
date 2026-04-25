package org.flexksx.platformapiservice.brandcontentitems.persistence;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ContentItemRepository extends JpaRepository<ContentItemEntity, String> {

  List<ContentItemEntity> findAllByBrandId(String brandId);

  Optional<ContentItemEntity> findByIdAndBrandId(String id, String brandId);
}
