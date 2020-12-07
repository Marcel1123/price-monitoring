package repositories.product;

import entities.ProductEntity;
import lombok.NoArgsConstructor;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.UUID;

@NoArgsConstructor
public class ProductRepository implements IProductRepository {
    private final EntityManager entityManager = Persistence.createEntityManagerFactory("price-monitoring").createEntityManager();

    @Override
    public void add(ProductEntity productEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        transaction.begin();
        this.entityManager.persist(productEntity);
        transaction.commit();
    }

    @Override
    public ProductEntity getById(UUID id) {
        return entityManager.find(ProductEntity.class, id);
    }
}
