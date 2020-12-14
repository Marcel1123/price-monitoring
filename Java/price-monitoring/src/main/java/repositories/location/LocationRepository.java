package repositories.location;

import entities.LocationEntity;
import lombok.AllArgsConstructor;

import javax.persistence.EntityManager;
import java.util.List;
import java.util.UUID;

@AllArgsConstructor
public class LocationRepository implements ILocationRepository {
    private EntityManager entityManager;

    @Override
    public List<LocationEntity> getAll() {
        return null;
    }

    @Override
    public void addCity(LocationEntity locationEntity) {

    }

    @Override
    public LocationEntity getById(UUID id) {
        return null;
    }

    @Override
    public List<LocationEntity> getByAddress(String address) {
        return null;
    }

    @Override
    public List<LocationEntity> getByCityId(UUID id) {
        return null;
    }
}
