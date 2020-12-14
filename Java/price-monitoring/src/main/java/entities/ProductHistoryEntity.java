package entities;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import util.enums.Currency;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.util.Date;
import java.util.UUID;

@Entity
@Table(name = "product_history")
@Data
public class ProductHistoryEntity {
    @Id
    @Column
    private UUID id;

    @Column
    private double price;

    @Column
    private Currency currency;

    @Column
    private Date date;
}
