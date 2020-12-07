package repositories.product;

import entities.ProductHistoryEntity;
import lombok.NoArgsConstructor;

import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.UUID;

@NoArgsConstructor
public class ProductHistoryRepository implements IProductHistoryRepository {
    private final EntityManager entityManager = Persistence.createEntityManagerFactory("price-monitoring").createEntityManager();

    @Override
    public void add(ProductHistoryEntity productHistoryEntity) {
        EntityTransaction transaction = this.entityManager.getTransaction();
        transaction.begin();
        this.entityManager.persist(productHistoryEntity);
        transaction.commit();
    }

    @Override
    public ProductHistoryEntity getById(UUID id) {
        return entityManager.find(ProductHistoryEntity.class, id);
    }
}
