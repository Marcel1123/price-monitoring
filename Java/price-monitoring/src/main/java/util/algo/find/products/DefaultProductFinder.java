package util.algo.find.products;

import entities.ProductEntity;
import lombok.NoArgsConstructor;
import util.enums.ProductType;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.criteria.*;
import java.util.List;
import java.util.UUID;

@NoArgsConstructor
@Named
@ApplicationScoped
public class DefaultProductFinder {
    @Inject
    private EntityManager entityManager;

    public List<ProductEntity> prepareQuery(ProductEntity productEntity){
        CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();

        CriteriaQuery<ProductEntity> query = criteriaBuilder.createQuery(ProductEntity.class);
        Root<ProductEntity> root = query.from(ProductEntity.class);

        Predicate predicateLocation = criteriaBuilder.equal(root.get("location"), productEntity.getLocation());
        Predicate predicateType = criteriaBuilder.equal(root.get("type"), productEntity.getType());

        query.select(root).where(criteriaBuilder.and(predicateLocation, predicateType));

        return entityManager.createQuery(query).getResultList();
    }
}
