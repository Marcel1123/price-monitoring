package repositories.product;

import entities.ProductHistoryEntity;
import lombok.NoArgsConstructor;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.EntityTransaction;
import javax.persistence.Persistence;
import java.util.UUID;


@Named
@ApplicationScoped
public class ProductHistoryRepository implements IProductHistoryRepository {
    @Inject
    private EntityManager entityManager;

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
